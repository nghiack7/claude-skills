/**
 * Tanca API Client for TypeScript/Bun
 *
 * Usage:
 *   import { TancaClient } from './tanca-client';
 *   const client = TancaClient.fromEnv();
 *   const employees = await client.fetchEmployees();
 */

export interface TancaConfig {
  baseUrl: string;
  token: string;
  deviceHeader: string;
  shopId: string;
  branchId: string;
  timezone: string;
}

export interface Employee {
  user_id: string;
  name: string;
  email: string;
  avatar?: string;
  code?: string;
}

export interface EmployeeShift {
  id: string;  // USE THIS for check-in/out
  shift_id: string;
  shift_assignment_id: string;
  date: string;
  check_in_time: string | null;
  check_out_time: string | null;
}

export interface CheckInOutResponse {
  success: boolean;
  message?: string;
  data?: unknown;
}

export class TancaClient {
  private config: TancaConfig;

  constructor(config: TancaConfig) {
    this.config = config;
  }

  static fromEnv(): TancaClient {
    const config: TancaConfig = {
      baseUrl: process.env.TANCA_API_URL || 'https://api.tanca.io/api/v4',
      token: process.env.TANCA_TOKEN || '',
      deviceHeader: process.env.TANCA_DEVICE_HEADER || '',
      shopId: process.env.TANCA_SHOP_ID || '',
      branchId: process.env.TANCA_BRANCH_ID || '',
      timezone: process.env.TANCA_TIMEZONE || 'Asia/Saigon',
    };

    if (!config.token) {
      throw new Error('TANCA_TOKEN environment variable is required');
    }

    return new TancaClient(config);
  }

  private headers(): HeadersInit {
    return {
      'authorization': this.config.token,
      'device': this.config.deviceHeader,
      'is-admin': '1',
      'lang': 'vi',
      'timezone': this.config.timezone,
      'Content-Type': 'application/json',
    };
  }

  private async get<T>(endpoint: string): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;
    const res = await fetch(url, { headers: this.headers() });

    if (!res.ok) {
      throw new Error(`Tanca API error: ${res.status} ${res.statusText}`);
    }

    return res.json();
  }

  private async post<T>(endpoint: string, body: unknown): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;
    const res = await fetch(url, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new Error(`Tanca API error: ${res.status} ${res.statusText}`);
    }

    return res.json();
  }

  // Employees

  async fetchEmployees(page = 1, limit = 100): Promise<{ data: Employee[]; total: number }> {
    return this.get(`/employee/list?page=${page}&limit=${limit}&is_inactive=0&is_no_need_timekeeping=0`);
  }

  async fetchAllEmployees(): Promise<Employee[]> {
    const all: Employee[] = [];
    let page = 1;
    const limit = 100;

    while (true) {
      const { data, total } = await this.fetchEmployees(page, limit);
      all.push(...data);

      if (page * limit >= total) break;
      page++;
    }

    return all;
  }

  // Shifts

  async getTodayShift(userId: string): Promise<EmployeeShift | null> {
    const today = new Date().toISOString().split('T')[0];
    return this.getShiftForDate(userId, today);
  }

  async getShiftForDate(userId: string, date: string): Promise<EmployeeShift | null> {
    const response = await this.get<{ data: EmployeeShift[] }>(
      `/shift/summary-employee-shift?user_id=${userId}&from_date=${date}&to_date=${date}`
    );
    return response.data?.[0] || null;
  }

  // Check-in/out

  async checkIn(employeeShiftId: string, reason = 'API check-in'): Promise<CheckInOutResponse> {
    return this.checkInOut(employeeShiftId, 'check_in', reason);
  }

  async checkOut(employeeShiftId: string, reason = 'API check-out'): Promise<CheckInOutResponse> {
    return this.checkInOut(employeeShiftId, 'check_out', reason);
  }

  async checkInOut(
    employeeShiftId: string,
    type: 'check_in' | 'check_out',
    reason: string,
    coords?: { latitude: number; longitude: number }
  ): Promise<CheckInOutResponse> {
    const body: Record<string, unknown> = {
      employee_shift_id: employeeShiftId,
      type,
      time: new Date().toISOString(),
      reason,
    };

    if (coords) {
      body.latitude = coords.latitude;
      body.longitude = coords.longitude;
    }

    return this.post('/shift/check-in-out-shift', body);
  }

  // Full workflow: auto check-in if not already checked in

  async autoCheckIn(userId: string, reason = 'Auto check-in'): Promise<{ success: boolean; message: string }> {
    const shift = await this.getTodayShift(userId);

    if (!shift) {
      return { success: false, message: 'No shift found for today' };
    }

    if (shift.check_in_time) {
      return { success: true, message: `Already checked in at ${shift.check_in_time}` };
    }

    await this.checkIn(shift.id, reason);
    return { success: true, message: 'Check-in recorded' };
  }

  async autoCheckOut(userId: string, reason = 'Auto check-out'): Promise<{ success: boolean; message: string }> {
    const shift = await this.getTodayShift(userId);

    if (!shift) {
      return { success: false, message: 'No shift found for today' };
    }

    if (!shift.check_in_time) {
      return { success: false, message: 'Not checked in yet' };
    }

    if (shift.check_out_time) {
      return { success: true, message: `Already checked out at ${shift.check_out_time}` };
    }

    await this.checkOut(shift.id, reason);
    return { success: true, message: 'Check-out recorded' };
  }
}

// CLI usage with Bun
if (import.meta.main) {
  const [command, ...args] = process.argv.slice(2);
  const client = TancaClient.fromEnv();

  switch (command) {
    case 'employees':
      console.log(JSON.stringify(await client.fetchAllEmployees(), null, 2));
      break;

    case 'shift':
      if (!args[0]) {
        console.error('Usage: bun tanca-client.ts shift <user_id>');
        process.exit(1);
      }
      console.log(JSON.stringify(await client.getTodayShift(args[0]), null, 2));
      break;

    case 'checkin':
      if (!args[0]) {
        console.error('Usage: bun tanca-client.ts checkin <user_id>');
        process.exit(1);
      }
      console.log(JSON.stringify(await client.autoCheckIn(args[0]), null, 2));
      break;

    case 'checkout':
      if (!args[0]) {
        console.error('Usage: bun tanca-client.ts checkout <user_id>');
        process.exit(1);
      }
      console.log(JSON.stringify(await client.autoCheckOut(args[0]), null, 2));
      break;

    default:
      console.log(`
Tanca API Client

Usage:
  bun tanca-client.ts employees           - List all employees
  bun tanca-client.ts shift <user_id>     - Get today's shift
  bun tanca-client.ts checkin <user_id>   - Auto check-in
  bun tanca-client.ts checkout <user_id>  - Auto check-out

Environment variables required:
  TANCA_TOKEN, TANCA_DEVICE_HEADER, TANCA_TIMEZONE
      `);
  }
}

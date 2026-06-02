#!/usr/bin/env fish

function infisical_export --description "Export Infisical secrets with path inheritance from parent to child"
    # Parse arguments using argparse for robust option handling
    argparse --name=infisical_export \
        'h/help' \
        'd/debug' \
        'projectId=' \
        'env=' \
        'path=' \
        'out=' \
        -- $argv
    or return 1

    # Show help if requested
    if set -q _flag_help
        echo "Usage: infisical_export --projectId <id> --env <env> --path <path> [--out <file>] [--debug]"
        echo ""
        echo "Export Infisical secrets with hierarchical path inheritance."
        echo "Variables from parent paths are inherited and can be overridden by child paths."
        echo ""
        echo "Options:"
        echo "  --projectId  Infisical project ID (required)"
        echo "  --env        Environment name (required)"
        echo "  --path       Target path (required)"
        echo "  --out        Output file path (optional, prints to stdout if not specified)"
        echo "  --debug, -d  Enable debug output"
        echo "  --help, -h   Show this help message"
        return 0
    end

    # Validate required arguments
    if not set -q _flag_projectId; or not set -q _flag_env; or not set -q _flag_path
        echo "Error: Missing required arguments" >&2
        echo "Usage: infisical_export --projectId <id> --env <env> --path <path>" >&2
        echo "Use --help for more information" >&2
        return 1
    end

    # Enable debug output if requested
    set -l debug_mode 0
    if set -q _flag_debug
        set debug_mode 1
    end

    # Split path into components and build path hierarchy
    set -l path_parts (string split "/" $_flag_path | string match -v "")
    set -l paths "/"

    # Build all parent paths from root to target
    set -l current_path ""
    for part in $path_parts
        set current_path "$current_path/$part"
        set -a paths $current_path
    end

    # Create temporary directory to store environment variables
    set -l temp_dir (mktemp -d)
    if test $status -ne 0
        echo "Error: Failed to create temporary directory" >&2
        return 1
    end

    # Use associative array for efficient merging (O(n) instead of O(n²))
    # Store all env vars in memory instead of repeatedly reading/writing files
    set -l env_keys
    set -l env_values

    # Export from each path level (parent to child)
    for current_path in $paths
        if test $debug_mode -eq 1
            echo "[DEBUG] Fetching env from path: $current_path" >&2
        else
            echo "Fetching env from path: $current_path" >&2
        end

        # Export to temporary file
        set -l temp_env_file "$temp_dir/env.tmp"

        # Try to export directly to file to preserve exact formatting
        infisical export --projectId=$_flag_projectId --env=$_flag_env --path=$current_path --format=dotenv > $temp_env_file 2>&1
        set -l export_status $status

        # Check if export succeeded
        if test $export_status -eq 0

            # If file has content, parse and merge variables
            if test -s $temp_env_file
                set -l var_count 0

                # Read line by line from the temp file
                while read -l line
                    # Skip empty lines and comments
                    if test -z "$line"; or string match -q "#*" -- $line
                        continue
                    end

                    # Extract key and value (split on first = only)
                    if string match -q -r '^[A-Z_][A-Z0-9_]*=' -- $line
                        set -l key_value (string split -m 1 "=" -- $line)
                        if test (count $key_value) -eq 2
                            set -l key $key_value[1]
                            set -l value $key_value[2]

                            # Remove surrounding quotes if present
                            set value (string trim -c '\'"' -- $value)

                            # Find if key already exists
                            set -l key_index (contains -i -- $key $env_keys)

                            if test -n "$key_index"
                                # Update existing value
                                set env_values[$key_index] $value
                                if test $debug_mode -eq 1
                                    echo "[DEBUG]   Overriding: $key" >&2
                                end
                            else
                                # Add new key-value pair
                                set -a env_keys $key
                                set -a env_values $value
                                if test $debug_mode -eq 1
                                    echo "[DEBUG]   Adding: $key" >&2
                                end
                            end

                            set var_count (math $var_count + 1)
                        end
                    end
                end < $temp_env_file

                if test $debug_mode -eq 1
                    echo "[DEBUG]   Found $var_count variables" >&2
                end
            else
                if test $debug_mode -eq 1
                    echo "[DEBUG]   No variables found at this path" >&2
                end
            end
        else
            # Check if it's just "no secrets found" error
            set -l error_msg (cat $temp_env_file 2>/dev/null)
            if not string match -q "*no secrets found*" -- $error_msg
                if test $debug_mode -eq 1
                    echo "[DEBUG]   Error fetching secrets: $error_msg" >&2
                end
            else
                if test $debug_mode -eq 1
                    echo "[DEBUG]   No secrets at this path (expected)" >&2
                end
            end
        end
    end

    # Output the final merged environment in dotenv format with export
    if test (count $env_keys) -gt 0
        # Determine output destination
        if set -q _flag_out
            # Output to file
            set -l output_file $_flag_out

            # Create output - each variable on its own line
            for i in (seq (count $env_keys))
                printf "export %s='%s'\n" $env_keys[$i] $env_values[$i]
            end > $output_file

            if test $status -eq 0
                echo "Environment variables exported to: $output_file" >&2
            else
                echo "Error: Failed to write to file: $output_file" >&2
                # Cleanup before returning
                if test -n "$temp_dir"; and test -d "$temp_dir"
                    rm -rf $temp_dir
                end
                return 1
            end
        else
            # Output to stdout - each variable on its own line
            for i in (seq (count $env_keys))
                printf "export %s='%s'\n" $env_keys[$i] $env_values[$i]
            end
        end
    else
        echo "Warning: No environment variables found" >&2
        # Cleanup before returning
        if test -n "$temp_dir"; and test -d "$temp_dir"
            rm -rf $temp_dir
        end
        return 1
    end

    # Cleanup temporary directory
    if test -n "$temp_dir"; and test -d "$temp_dir"
        rm -rf $temp_dir
    end

    return 0
end

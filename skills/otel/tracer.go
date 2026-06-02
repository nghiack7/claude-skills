// Reference implementation: internal/otel/tracer.go
// Copy this file when adding OTEL to a new Lambda function

package otel

import (
	"context"
	"log"
	"os"
	"time"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/sqs"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
	"go.opentelemetry.io/otel/trace"
)

const (
	defaultOtelTimeout        = 2 * time.Second
	defaultFlushTimeout       = 2 * time.Second
	defaultBatchTimeout       = 1 * time.Second
	defaultMaxQueueSize       = 100
	defaultMaxExportBatchSize = 50
)

type TracerProviderFlusher struct {
	*sdktrace.TracerProvider
}

func (tp *TracerProviderFlusher) ForceFlush(ctx context.Context) error {
	if tp.TracerProvider == nil {
		return nil
	}
	flushCtx, cancel := context.WithTimeout(ctx, defaultFlushTimeout)
	defer cancel()
	if err := tp.TracerProvider.ForceFlush(flushCtx); err != nil {
		log.Printf("[OTEL] ForceFlush error (ignored): %v", err)
	}
	return nil
}

func (tp *TracerProviderFlusher) Shutdown(ctx context.Context) error {
	if tp.TracerProvider == nil {
		return nil
	}
	shutdownCtx, cancel := context.WithTimeout(ctx, defaultFlushTimeout)
	defer cancel()
	if err := tp.TracerProvider.Shutdown(shutdownCtx); err != nil {
		log.Printf("[OTEL] Shutdown error (ignored): %v", err)
	}
	return nil
}

func Init(ctx context.Context, serviceName string) *TracerProviderFlusher {
	endpoint := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
	if os.Getenv("OTEL_SDK_DISABLED") == "true" || endpoint == "" {
		return &TracerProviderFlusher{}
	}

	// IMPORTANT: Must explicitly pass endpoint via WithEndpoint().
	// Do NOT rely on library auto-reading OTEL_EXPORTER_OTLP_ENDPOINT env var -
	// it breaks with gRPC resolver changes (delegating_resolver: invalid target address).
	exporter, err := otlptracegrpc.New(ctx,
		otlptracegrpc.WithEndpoint(endpoint),
		otlptracegrpc.WithTimeout(defaultOtelTimeout),
		otlptracegrpc.WithRetry(otlptracegrpc.RetryConfig{Enabled: false}),
	)
	if err != nil {
		log.Printf("[OTEL] Failed to create exporter: %v", err)
		return &TracerProviderFlusher{}
	}

	// serviceName is the default; resource.WithFromEnv() overrides with OTEL_SERVICE_NAME if set
	attrs := []attribute.KeyValue{semconv.ServiceNameKey.String(serviceName)}
	if version := os.Getenv("SERVICE_VERSION"); version != "" {
		attrs = append(attrs, semconv.ServiceVersionKey.String(version))
	}

	res, err := resource.New(ctx, resource.WithAttributes(attrs...), resource.WithFromEnv())
	if err != nil {
		log.Printf("[OTEL] Failed to create resource: %v", err)
		return &TracerProviderFlusher{}
	}

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithSpanProcessor(sdktrace.NewBatchSpanProcessor(exporter,
			sdktrace.WithBatchTimeout(defaultBatchTimeout),
			sdktrace.WithExportTimeout(defaultOtelTimeout),
			sdktrace.WithMaxQueueSize(defaultMaxQueueSize),
			sdktrace.WithMaxExportBatchSize(defaultMaxExportBatchSize),
		)),
		sdktrace.WithResource(res),
		sdktrace.WithSampler(sdktrace.AlwaysSample()),
	)

	otel.SetTracerProvider(tp)
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
		propagation.TraceContext{},
		propagation.Baggage{},
	))

	return &TracerProviderFlusher{TracerProvider: tp}
}

func StartSpan(ctx context.Context, name string, opts ...trace.SpanStartOption) (context.Context, trace.Span) {
	return otel.Tracer("").Start(ctx, name, opts...)
}

// SQS trace propagation helpers

func InjectToSQSAttributes(ctx context.Context) map[string]*sqs.MessageAttributeValue {
	carrier := propagation.MapCarrier{}
	otel.GetTextMapPropagator().Inject(ctx, carrier)
	if len(carrier) == 0 {
		return nil
	}
	attrs := make(map[string]*sqs.MessageAttributeValue, len(carrier))
	for k, v := range carrier {
		attrs[k] = &sqs.MessageAttributeValue{
			DataType:    aws.String("String"),
			StringValue: aws.String(v),
		}
	}
	return attrs
}

func ExtractFromSQSRecord(ctx context.Context, record events.SQSMessage) context.Context {
	if len(record.MessageAttributes) == 0 {
		return ctx
	}
	carrier := propagation.MapCarrier{}
	for k, v := range record.MessageAttributes {
		if v.StringValue != nil {
			carrier[k] = *v.StringValue
		}
	}
	return otel.GetTextMapPropagator().Extract(ctx, carrier)
}

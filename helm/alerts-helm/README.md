# alerts-helm

A Helm chart for deploying custom alerts and monitoring for your CIRRUS applications. This chart provides templates for configuring Prometheus alerts, Alertmanager routing, and custom metrics collection.

## Overview

CIRRUS provides monitoring through Prometheus and Alertmanager. These examples enable you to create custom alerts tailored to your application's specific needs.

## Prerequisites

Before deploying custom alerts, ensure:

- Your application is already deployed and syncing with Argo CD
- You have a Helm chart repository configured for your application
- Your application namespace is set up in the CIRRUS cluster

> **Note:** These alert templates are designed to be added to your existing application Helm chart, not deployed as a standalone chart. Copy the templates you need into your application's `templates/` directory.

## What's Included

This chart provides templates for:

| Template | Purpose |
|----------|---------|
| **alertmanager-config.yaml** | Routes alerts to notification channels (email, Slack, etc.) |
| **prometheus-rule.yaml** | Defines alert conditions and thresholds |
| **pod-monitor.yaml** | Collects metrics directly from pods |
| **service-monitor.yaml** | Collects metrics from a Kubernetes Service |

## Configuration

Update `values.yaml` with your alerting details:

```yaml
appName: my-app
namespace: my-namespace
alertEmail: team@ucar.edu
```

## AlertmanagerConfig

The `alertmanager-config.yaml` template configures how alerts are routed and where notifications are sent.

### Key Configuration Options

- **`groupBy`** — Groups alerts by specified labels (e.g., `alertname`, `severity`)
- **`groupWait`** — How long to wait before sending the first notification for a new alert group
- **`groupInterval`** — How long to wait before sending updates about an existing alert group
- **`repeatInterval`** — How long to wait before resending an alert that has already fired
- **`matchers`** — Filters which alerts this configuration applies to (typically by namespace)

### Alternative Receivers

The template includes email configuration by default. Alertmanager supports multiple notification channels:

- **Slack** — Send alerts to Slack channels
- **PagerDuty** — Integrate with on-call scheduling
- **Webhook** — Send alerts to custom HTTP endpoints
- **OpsGenie** — Route to incident management platforms
- **Microsoft Teams** — Post to Teams channels

For complete receiver configuration options, see the [Prometheus Alerting documentation](https://prometheus.io/docs/alerting/latest/configuration/).

## PrometheusRule

The `prometheus-rule.yaml` template defines the conditions that trigger alerts. It includes example rules for:

- **PodDown** — Alerts when a pod is unavailable
- **HighMemoryUsage** — Alerts when memory usage exceeds 90%
- **HighCPUUsage** — Alerts when CPU usage is above 80%
- **TestAlert** — An always-firing test alert using `vector(1)` for initial setup validation

### Alert Rule Components

- **`alert`** — Name of the alert
- **`expr`** — PromQL expression that defines when the alert fires
- **`for`** — How long the condition must be true before firing
- **`labels`** — Metadata attached to the alert (used for routing and grouping)
- **`annotations`** — Human-readable information included in notifications

> **Testing tip:** Use the `TestAlert` rule with `expr: vector(1)` when first setting up alerts. This always-firing alert verifies your notification pipeline works correctly. Remove it once confirmed working.

## Monitoring Templates

### PodMonitor

The `pod-monitor.yaml` template tells Prometheus to scrape metrics directly from pods matching specific labels. Use this when your application exposes metrics on a specific port.

### ServiceMonitor

The `service-monitor.yaml` template scrapes metrics from a Kubernetes Service instead of individual pods. This is useful when you have a Service fronting your application.

> **Note:** Your application must expose a metrics endpoint that returns data in Prometheus format. Popular libraries include `prometheus_client` (Python), `prom-client` (Node.js), Micrometer (Java), and `prometheus/client_golang` (Go).

## Testing Your Alerts

!!! important
    CIRRUS does not expose Alertmanager directly to users. You cannot view Alertmanager logs or use the Alertmanager UI. This makes proper testing during initial setup crucial.

### Recommended Testing Workflow

1. **Add the test alert** — Use the included `TestAlert` with `expr: vector(1)` (always fires)
2. **Deploy the changes** — Push to your repository and let Argo CD sync
3. **Wait for notification** — You should receive an alert immediately
4. **Verify notification content** — Check that formatting and routing are correct
5. **Remove the test alert** — Delete the `TestAlert` rule from your PrometheusRule
6. **Deploy again** — Push the updated configuration

The `vector(1)` expression always evaluates to true, ensuring the alert fires immediately without having to trigger actual error conditions.

## Deployment

1. **Copy templates** to your existing Helm chart's `templates/` directory
2. **Update values.yaml** with your configuration
3. **Commit and push** changes to your Git repository
4. **Argo CD will automatically sync** the changes to your application

## Troubleshooting

### Alerts Not Firing

- Verify the PromQL expression using Prometheus query interface
- Check that metrics are being collected (PodMonitor/ServiceMonitor configured correctly)
- Ensure the `for` duration has elapsed
- Confirm namespace matchers align with your application's namespace

### Notifications Not Received

- Verify AlertmanagerConfig matchers correctly select your alerts
- Check receiver configuration (email addresses, webhook URLs, etc.)
- Confirm the `repeatInterval` hasn't suppressed duplicate notifications

### Metrics Not Available

- Confirm your application exposes metrics on the configured port and path
- Check PodMonitor/ServiceMonitor selector labels match your pod labels
- Verify the metrics port is defined in your Service manifest

## Additional Resources

- [Prometheus Alerting Documentation](https://prometheus.io/docs/alerting/latest/configuration/)
- [Prometheus Query Language (PromQL)](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [CIRRUS Documentation](https://cirrus.ucar.edu/)

For assistance with custom alerting configuration, see the [CIRRUS documentation on custom alerting](https://cirrus.ucar.edu/cloud/09-monitoring-applications/custom-alerts/).
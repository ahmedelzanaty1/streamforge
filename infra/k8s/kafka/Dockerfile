FROM confluentinc/cp-kafka:7.6.0

USER root

# Create directory for JMX agent
RUN mkdir -p /opt/jmx

# Copy JMX Prometheus Java Agent
COPY jmx_prometheus_javaagent-0.20.0.jar /opt/jmx/jmx_prometheus_javaagent.jar

# Fix permissions (important)
RUN chown -R appuser:appuser /opt/jmx

USER appuser

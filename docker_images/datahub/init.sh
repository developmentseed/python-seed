echo ======================================================================================
echo STARTING DATAHUB:
env
echo =======================================================================================

datahub run --config ./config.yaml isharp.datahub.broker_service.server:DataBrokerService

data
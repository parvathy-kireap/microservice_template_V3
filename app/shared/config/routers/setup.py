from app.shared.config.endpoints.tags import EndpointTag


class RouterSetup:
    class Router:
        def __init__(self, prefix: str, tag: str):
            self.prefix = prefix
            self.tag = tag

    sample_router_v0 = Router(prefix='/sample/V0',
                              tag=EndpointTag.sample_V0)
    
class SqlRouterSetUp:
    class Router:
        def __init__(self, prefix:str, tag: str):
            self.prefix = prefix
            self.tag = tag
    
    sql_sample_router = Router(prefix='/sql/sample', tag=EndpointTag.sql_sample)

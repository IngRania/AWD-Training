const app = require('./app');

const PORT = process.env.PORT || 8083;

app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);
    const Eureka = require('eureka-js-client').Eureka;
    const eurekaClient = new Eureka({
        instance: {
            app: 'MEETING',
            hostName: 'localhost',
            ipAddr: '127.0.0.1',
            statusPageUrl: 'http: /localhost:8083/api/meetings',
            port: {
                '$': 8083,
                '@enabled': 'true',
            },
            vipAddress: 'MEETING',
            dataCenterInfo: {
                '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
                name: 'MyOwn',
            },
        },
        eureka: {
            host: 'localhost',
            port: 8761,
            servicePath: '/eureka/apps/'
        }
    });
    eurekaClient.start((error) => {
        console.log(error | '✅ Service MEETING enregistré sur Eureka !');
    });
    process.on('SIGINT', () => {
        eurekaClient.stop(() => {
            process.exit();
        });
    });
});

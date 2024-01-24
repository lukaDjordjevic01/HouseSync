export function getGrafanaURL(deviceId: string, measurement: string, from="now-1h"): string{
    if (deviceId.includes("DHT"))
        return  "http://localhost:3000/d-solo/ce656564-eee0-4afc-9131-027b50a2ed77" +
            "/house-sync-dashboard?orgId=1&refresh=5s&from=" + from + "&to=now&panelId=1" +
             "&var-dhtDeviceId=" + deviceId + "&var-dhtMeasurement=" + measurement
    else if (deviceId.includes("DS"))
        return  "http://localhost:3000/d-solo/ce656564-eee0-4afc-9131-027b50a2ed77" +
            "/house-sync-dashboard?orgId=1&refresh=5s&from=" + from + "&to=now&panelId=4" +
            "&var-dsDeviceId=" + deviceId
    else if (deviceId.includes("PIR"))
        return  "http://localhost:3000/d-solo/ce656564-eee0-4afc-9131-027b50a2ed77" +
            "/house-sync-dashboard?orgId=1&refresh=5s&from=" + from + "&to=now&panelId=3&" +
            "var-pirDeviceId=" + deviceId
    else if (deviceId.includes("DUS"))
        return  "http://localhost:3000/d-solo/ce656564-eee0-4afc-9131-027b50a2ed77" +
            "/house-sync-dashboard?orgId=1&refresh=5s&from=" + from + "&to=now&panelId=2&" +
            "var-dusDeviceId=" + deviceId
    else if (deviceId.includes("DMS"))
        return  "http://localhost:3000/d-solo/ce656564-eee0-4afc-9131-027b50a2ed77" +
            "/house-sync-dashboard?orgId=1&refresh=5s&from=" + from + "&to=now&panelId=5"
    else if (deviceId.includes("GSG"))
        return  "http://localhost:3000/d-solo/ce656564-eee0-4afc-9131-027b50a2ed77" +
            "/house-sync-dashboard?orgId=1&refresh=5s&from=" + from + "&to=now&panelId=6&" +
            "var-gsgMeasurement=" + measurement
    else if (deviceId.includes("ALARMS"))
        return  "http://localhost:3000/d-solo/ce656564-eee0-4afc-9131-027b50a2ed77/house-sync-dashboard?orgId=1&" +
            "refresh=5s&tab=query&from=" + from + "&to=now&panelId=7"
}
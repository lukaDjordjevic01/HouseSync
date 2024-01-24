import {Device, Measurement} from "../model.ts";
import {useEffect, useState} from "react";
import {io} from "socket.io-client";
import {getGrafanaURL} from "../util/util.ts";
import {Box, useTheme} from "@mui/material";
import "./device-popup.css";
import DateTimeRangePicker from "./date-time-range-picker.tsx";

export default function DevicePopup({device}: {device: Device}) {

    const [measurements, setMeasurements] = useState<Measurement[]>([]);
    const [timeSpanFrom, setTimeSpanFrom] = useState<string>("-1h");
    const theme = useTheme();

    useEffect(() => {
        const socket = io('http://localhost:5000');
        const topic = device.id

        if (device.id.includes("DHT")) setMeasurements(
            [{
                name: "Temperature", unit: "°C"
            }, {
                name: "Humidity", unit: "%"
            }])
        else if (device.id.includes("GSG")) setMeasurements(
            [{
                name: "Acceleration", unit: "x y z"
            }, {
                name: "Rotation", unit: "x y z"
            }])

        socket.emit('subscribe', { topic });

        const handler = (data: any) => {
            console.log(data);
        }

        // Listen for messages on the subscribed topic
        socket.off('message', handler).on('message', handler);

        return () => {
            socket.emit('unsubscribe', { topic });
            console.log("Unmounted")
            socket.disconnect();
        };
    }, [device]);

    return (
        <Box id="device-popup-box"
            sx={{
                backgroundColor: theme.palette.background.default,
                color: theme.palette.primary.contrastText,
                borderColor: theme.palette.primary.contrastText
            }}
        >
            <h2>{device.name}</h2>

            <DateTimeRangePicker timeChangeAction={setTimeSpanFrom}/>
            {device && !device.id.includes("DHT") && !device.id.includes("GSG") &&
                <Box className="grafana-box">
                    <iframe src={getGrafanaURL(device.id, "", `now${timeSpanFrom}`)}/>
                </Box>
            }

            {device && measurements[0] && measurements[1] && (device.id.includes("DHT") || device.id.includes("GSG")) &&
                <Box className="grafana-box">
                    <h3>{measurements[0].name} {measurements[0].unit}</h3>
                    <iframe src={getGrafanaURL(device.id, measurements[0].name, `now${timeSpanFrom}`)}/>

                    <h3>{measurements[1].name} {measurements[1].unit}</h3>
                    <iframe src={getGrafanaURL(device.id, measurements[1].name, `now${timeSpanFrom}`)}/>
                </Box>
            }
        </Box>
    )
}
import {Device} from "../model.ts";
import {useEffect} from "react";
import {io} from "socket.io-client";

export default function DevicePopup({device}: {device: Device}) {

    useEffect(() => {
        const socket = io('http://localhost:5000');
        const topic = device.id

        socket.emit('subscribe', { topic });

        const handler = (data: any) => {
            // console.log(data);
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
        <>
            <p>{device.name}</p>
        </>
    )
}
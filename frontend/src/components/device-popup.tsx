import {Device} from "../model.ts";

export default function DevicePopup({device}: {device: Device}) {
    return (
        <>
            <p>{device.name}</p>
        </>
    )
}
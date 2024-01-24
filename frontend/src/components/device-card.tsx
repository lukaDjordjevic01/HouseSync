import {Device} from "../model.ts";
import {Box, Typography, useTheme} from "@mui/material";
import {useEffect, useState} from "react";

export default function DeviceCard({device, setSelectedDevice}: {device: Device,
    setSelectedDevice: (selectedDevice: Device) => void
})  {

    const theme = useTheme();

    const [image, setImage] = useState<string>("");

    useEffect(() => {
        const imageBase = "src/assets";

        if (device.id.includes("DHT")) setImage(`${imageBase}/ambientSensor.jpg`)
        else if (device.id.includes("DUS")) setImage(`${imageBase}/dus.jpeg`)
        else if (device.id.includes("IR")) setImage(`${imageBase}/pir.jpg`)
        else if (device.id.includes("DMS")) setImage(`${imageBase}/dms.jpg`)
        else if (device.id.includes("DL")) setImage(`${imageBase}/dl.jpg`)
        else if (device.id.includes("LCD")) setImage(`${imageBase}/lcd.jpg`)
        else if (device.id.includes("GSG")) setImage(`${imageBase}/gsg.jpg`)
        else if (device.id.includes("RGB")) setImage(`${imageBase}/rgb.jpg`)
        else if (device.id.includes("RECEIVER")) setImage(`${imageBase}/receiver.jpg`)
        else if (device.id.includes("DS")) setImage(`${imageBase}/ds.jpeg`)
        else if (device.id.includes("B4SD")) setImage(`${imageBase}/b4sd.jpeg`)
        else if (device.id.includes("DB") || device.id.includes("BB")) setImage(`${imageBase}/db.jpg`)
        else setImage(`${imageBase}/ambientSensor.jpg`)
    }, [device])

    return (
        <Box
            onClick={() => setSelectedDevice(device)}
            sx={{
                backgroundColor: theme.palette.background.default,
                padding: "10px",
                borderRadius: "5px",
                width: "15%",
                "&:hover": {
                    cursor: "pointer",
                    opacity: "70%"
                },
                height: "30vh"
            }}
        >
            <img src={image}
                 alt={"Loading..."}
                 style={{
                    width: "100%",
                     height: "70%"
                }}
            />
            <Typography>Id: {device.id}</Typography>
            <Typography>Name: {device.name}</Typography>
        </Box>
    )
}

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
                }
            }}
        >
            <img src={image}
                 alt={"Loading..."}
                 style={{
                    width: "100%",
                }}
            />
            <Typography>Id: {device.id}</Typography>
            <Typography>Name: {device.name}</Typography>
        </Box>
    )
}

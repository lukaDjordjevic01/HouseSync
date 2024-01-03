import React, {useEffect, useState} from "react";
import {Device} from "../model.ts";
import axios from 'axios';
import {Box, Dialog, DialogContent, useTheme} from "@mui/material";
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import DeviceCard from "../components/device-card.tsx";
import DevicePopup from "../components/device-popup.tsx";

export default function Devices () {

    const theme = useTheme();

    const [pi1Devices, setPi1Devices] = useState<Device[]>([]);
    const [pi2Devices, setPi2Devices] = useState<Device[]>([]);
    const [pi3Devices, setPi3Devices] = useState<Device[]>([]);

    const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);

    useEffect(() => {
        axios.get<Device[]>("http://localhost:5000/get-devices")
            .then(res => {
                if (res.status === 200) {
                    setPi1Devices(res.data.filter((device) => {
                        if (device.runs_on === "PI1") return device;
                    }))
                    setPi2Devices(res.data.filter((device) => {
                        if (device.runs_on === "PI2") return device;
                    }))
                    setPi3Devices(res.data.filter((device) => {
                        if (device.runs_on === "PI3") return device;
                    }))
                }
            })
            .catch(err => {
                console.log(err);
            })
    }, [])

    return(
        <Box sx={{
            display: "flex",
            flexDirection: "column",
            padding: "20px",
            gap: "10px"
        }}>
            <Accordion
                sx={{
                    backgroundColor: theme.palette.primary.main,
                    color: theme.palette.primary.contrastText,
                }}
            >
                <AccordionSummary>Pi 1</AccordionSummary>
                <AccordionDetails sx={{
                    display: "flex",
                    flexWrap: 'wrap',
                    justifyContent: "stretch",
                    gap: "15px"
                }}>
                    {pi1Devices.map(device =>
                      <DeviceCard key={device.id} device={device} setSelectedDevice={setSelectedDevice}/>
                    )}
                </AccordionDetails>
            </Accordion>
            <Accordion
                sx={{
                    backgroundColor: theme.palette.primary.main,
                    color: theme.palette.primary.contrastText
                }}
            >
                <AccordionSummary>Pi 2</AccordionSummary>
                <AccordionDetails sx={{
                    display: "flex",
                    flexWrap: 'wrap',
                    justifyContent: "stretch",
                    gap: "15px"
                }}>
                    {pi2Devices.map(device =>
                        <DeviceCard key={device.id} device={device} setSelectedDevice={setSelectedDevice}/>
                    )}
                </AccordionDetails>
            </Accordion>
            <Accordion
                sx={{
                    backgroundColor: theme.palette.primary.main,
                    color: theme.palette.primary.contrastText
                }}
            >
                <AccordionSummary>Pi 3</AccordionSummary>
                <AccordionDetails sx={{
                    display: "flex",
                    flexWrap: 'wrap',
                    justifyContent: "stretch",
                    gap: "15px"
                }}>
                    {pi3Devices.map(device =>
                        <DeviceCard key={device.id} device={device} setSelectedDevice={setSelectedDevice}/>
                    )}
                </AccordionDetails>
            </Accordion>

            <Dialog open={selectedDevice !== null} onClose={() => setSelectedDevice(null)} fullWidth>
                <DialogContent>
                    {selectedDevice && <DevicePopup device={selectedDevice}/>}
                </DialogContent>
            </Dialog>
        </Box>
    )
}
import React, {useEffect, useState} from "react";
import {Device} from "../model.ts";
import axios from 'axios';
import {Box} from "@mui/material";
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';

export default function Devices () {

    const [pi1Devices, setPi1Devices] = useState<Device[]>([]);
    const [pi2Devices, setPi2Devices] = useState<Device[]>([]);
    const [pi3Devices, setPi3Devices] = useState<Device[]>([]);

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
        <Box>
            <Accordion>
                <AccordionSummary>Pi 1</AccordionSummary>
                <AccordionDetails>
                    {pi1Devices.map(device =>
                      <p>{device.name}</p>
                    )}
                </AccordionDetails>
            </Accordion>
            <Accordion>
                <AccordionSummary>Pi 2</AccordionSummary>
                <AccordionDetails>
                    {pi2Devices.map(device =>
                        <p>{device.name}</p>
                    )}
                </AccordionDetails>
            </Accordion>
            <Accordion>
                <AccordionSummary>Pi 3</AccordionSummary>
                <AccordionDetails>
                    {pi3Devices.map(device =>
                        <p>{device.name}</p>
                    )}
                </AccordionDetails>
            </Accordion>
        </Box>
    )
}
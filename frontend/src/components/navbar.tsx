import {AppBar, Button, Toolbar, Typography} from "@mui/material";
import {Outlet, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {io} from "socket.io-client";
import axios from "axios";

export default function Navbar () {
    const navigate = useNavigate()

    const [peopleInside, setPeopleInside] = useState<number>(0);
    const [alarmSystemIsActive, setAlarmSystemIsActive] = useState<boolean>(false);

    const getPeopleInside = () => {
        axios.get<PeopleInside>("http://localhost:5000/people-inside")
            .then(res => {
                if (res.status === 200) {
                    setPeopleInside(res.data.people_inside);
                }
            })
            .catch(err => {
                console.log(err);
            });
    };
    const getAlarmSystemIsActive = () => {
        axios.get<AlarmSystemIsActive>("http://localhost:5000/alarm-system-is-active")
            .then(res => {
                if (res.status === 200) {
                    setAlarmSystemIsActive(res.data.alarm_system_is_active);
                }
            })
            .catch(err => {
                console.log(err);
            });
    };
    
    useEffect(() => {

        getPeopleInside();
        getAlarmSystemIsActive();

        const socket = io('http://localhost:5000');
        socket.emit('subscribe', { topic: "people-inside"});
        socket.emit('subscribe', { topic: "alarm-system-activation" });

        const handleMessage = (data) => {
            if (data.topic === "people-inside"){
                setPeopleInside(data.message.people_inside);
            } else if (data.topic === "alarm-system-activation") {
                setAlarmSystemIsActive(data.message.alarm_system_is_active);
            }
        }
        socket.off('message', handleMessage).on('message', handleMessage);
        
        return () => {
            socket.emit('unsubscribe', { topic: "people-inside" });
            socket.emit('unsubscribe', { topic: "alarm-system-activation" });
            console.log("Unmounted")
            socket.disconnect();
        };
    }, []);
    
    return (
        <div style={{height: "100%", width: "100%", display: "flex", flexDirection: "column"}}>
            <AppBar position={'relative'} style={{flex: '0 1 auto'}}>
                <Toolbar sx={{
                    display: "flex"
                }}>
                    <div style={{
                        width: "300px",
                        height: "100px"
                    }}>
                        <h1>House Sync</h1>
                    </div>

                    <Button onClick={() => navigate('/alarms')}
                            sx={{
                                textTransform: "capitalize",
                                color: "#F5F5F5"
                            }}>Alarms</Button>

                    <Button onClick={() => navigate('/devices')}
                            sx={{
                                textTransform: "capitalize",
                                color: "#F5F5F5"
                            }}>Devices</Button>

                    <Button onClick={() => navigate('/scenarios')}
                            sx={{
                              textTransform: "capitalize",
                              color: "#F5F5F5"
                            }}>Scenarios</Button>

                    <Button onClick={() => navigate('/bedroom-and-garage')}
                            sx={{
                                textTransform: "capitalize",
                                color: "#F5F5F5"
                            }}>Bedroom and garage</Button>
                    
                    <Typography
                        sx={{
                            flexGrow: "1",
                            textAlign: "right"
                        }}
                    >People inside the house: {peopleInside}, Alarm system: {alarmSystemIsActive ? "Active"
                        : "Inactive"}</Typography>
                    
                </Toolbar>
            </AppBar>
            <div id="detail" style={{flex: '1 1 auto', width: "100%", overflow: "auto"}}>
                <Outlet/>
            </div>
        </div>
    )
}

interface PeopleInside {
    people_inside: number
}

interface AlarmSystemIsActive {
    alarm_system_is_active: boolean
}
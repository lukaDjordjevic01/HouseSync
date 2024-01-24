import {AppBar, Button, Toolbar, Typography} from "@mui/material";
import {Outlet, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {io} from "socket.io-client";

export default function Navbar () {
    const navigate = useNavigate()
    
    const [peopleInside, setPeopleInside] = useState<number>(0);
    
    useEffect(() => {
        const socket = io('http://localhost:5000');
        const topic: string = "people-inside";
        socket.emit('subscribe', { topic });
        
        const handlePeopleInside = (data) => {
            setPeopleInside(data.message.people_inside);
        }
        socket.off('message', handlePeopleInside).on('message', handlePeopleInside);
        
        return () => {
            socket.emit('unsubscribe', { topic });
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
                    >People inside the house: {peopleInside}</Typography>
                    
                </Toolbar>
            </AppBar>
            <div id="detail" style={{flex: '1 1 auto', width: "100%", overflow: "auto"}}>
                <Outlet/>
            </div>
        </div>
    )
}
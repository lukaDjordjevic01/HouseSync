import {AppBar, Button, Toolbar} from "@mui/material";
import {Outlet, useNavigate} from "react-router-dom";

export default function Navbar () {
    const navigate = useNavigate()

    return (
        <div style={{height: "100%", width: "100%", display: "flex", flexDirection: "column"}}>
            <AppBar position={'relative'} style={{flex: '0 1 auto'}}>
                <Toolbar>
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

                </Toolbar>
            </AppBar>
            <div id="detail" style={{flex: '1 1 auto', width: "100%"}}>
                <Outlet/>
            </div>
        </div>
    )
}
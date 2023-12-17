import * as React from 'react';
import Popover from '@mui/material/Popover';
import Typography from '@mui/material/Typography';
import IconButton from "@mui/material/IconButton";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import InfoIcon from '@mui/icons-material/Info';
import Button from "@mui/material/Button";

import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import GameDay from "../model/GameDay";
import {details_style} from "./Styles";


interface IProps {
    gameDay: GameDay,
}

export default function Details(props : IProps) {
    const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null);

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
        event.stopPropagation();
    };

    const handleClose = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(null);
        event.stopPropagation();
    };

    const open = Boolean(anchorEl);
    const id = open ? 'simple-popover' : undefined;
    const dateString = props.gameDay.date.toLocaleString('en-us', {month: "long", day: 'numeric'});

    return (
        <React.Fragment>
            <Button sx={details_style.date} variant="outlined" onClick={handleClick}>
                {props.gameDay.date.toLocaleString('en-us', {day: 'numeric'})}
            </Button>
            <Popover
                id={id}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'center',
                }}
            >
                <TextField
                    id="filled-multiline-static"
                    label={`${dateString} Schedule and Scores`}
                    multiline
                    defaultValue={props.gameDay.toString()}
                    variant="filled"
                    inputProps={
                        { readOnly: true, }
                    }
                    sx = {details_style.text_field}
                />
            </Popover>
        </React.Fragment>
    );
}
import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import {calendar_style} from "./Styles";
import Thermometer from "./Thermometer";
import GameDay from "../model/GameDay";
import Details from "./Details";

interface IDayProps {
    gameDay: GameDay,
    disable: boolean,
    selected: boolean,
    onSelect: () => void,
}

export default function Day(props: IDayProps) {
    const getDayStyle = () => {
        if(props.disable) {
            return calendar_style.day_disabled;
        }
        if(props.selected) {
            return calendar_style.day_selected;
        }
        return calendar_style.day;
    }

    const _handleClick = () => {
        if(!props.disable) {
            props.onSelect();
        }
    }

    return (
        <Box sx={getDayStyle()}  onClick={_handleClick}>
            {!props.disable && <Thermometer gameDay = {props.gameDay}/>}
            {!props.disable && <Box sx={calendar_style.details}>
                <Details gameDay={props.gameDay}/>
            </Box>}
        </Box>
    );
}
import * as React from 'react';
import Box from '@mui/material/Box';
import {thermometer_style} from "./Styles";
import {Math_range} from "../utility/MathPlus";
import GameDay from "../model/GameDay";
import Details from "./Details";

const THERMOMETER_COLORS1 = [
    "#FFFFFF",
    "#E2F7E2",
    "#E2F7E2",
    "#E2F7E2",
    "#C5F0C5",
    "#A7E8A8",
    "#8AE08B",
    "#6DD86E",
    "#50D151",
    "#32C934",
    "#15C117"];

const THERMOMETER_COLORS = [
    "#E00000",
    "#fcba03",
    "#F0F000",
    "#b1fc03",
    "#00E000"];

const MIN_SCORE = 0;
const MAX_SCORE = 30;

interface IProps {
    gameDay: GameDay,
}

export default function Thermometer(props: IProps) {

    const f = React.useMemo(() => {
        return Math_range((props.gameDay.score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE), 0, 0.999);
    }, [props.gameDay]);

    const backgroundColor = React.useMemo(() => {
        return THERMOMETER_COLORS[Math.floor(f * THERMOMETER_COLORS.length)];
    }, [f]);

    return (
        <Box sx={thermometer_style.container}>
            <Box sx={thermometer_style.tube}/>
            <Box sx={thermometer_style.bulb}/>
            <Box sx={{...thermometer_style.tube_inner}}>
                <Box sx={{...thermometer_style.tube_fill, backgroundColor, height: f}}/>
            </Box>
            <Box sx={{...thermometer_style.bulb_inner, backgroundColor}}/>
        </Box>
    )
}

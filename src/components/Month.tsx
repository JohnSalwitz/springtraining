import * as React from 'react';
import Box from '@mui/material/Box';
import Day from "./Day";
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import {calendar_style} from "./Styles";
import {DatePlus} from "../utility/DatePlus";
import GameDay from "../model/GameDay";
import {schedule} from "../model/test_data/schedule_2024";

const _daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
const _day0 = new DatePlus(2024, 2, 1);
const _dayOffset = _day0.getDay();

export default function Month() {

    const [selected, setSelected] = React.useState<Array<number>>([]);

    function _handleSelect(_date : DatePlus) {
        if(selected.includes(_date.dayOfYear())) {
            setSelected(selected.filter((d: number) => d !== _date.dayOfYear()));
        } else {
            setSelected([...selected, _date.dayOfYear()]);
        }
    }

    function _renderDay(_week: number, _day: number): React.ReactElement {
        const _dayIndex = _week * 7 + _day - _dayOffset;
        const _date = _day0.addDays(_dayIndex);
        return <Day
            gameDay={new GameDay(schedule, _date)}
            disable={_day0.getMonth() !== _date.getMonth()}
            selected={selected.includes(_date.dayOfYear())}
            onSelect={() => _handleSelect(_date)}
        />;
    }

    return (
        <Stack>
            <Box sx={calendar_style.title}>
                <Typography variant="h3">
                    {_day0.toLocaleString('en-us',{month: "long", year:'numeric'})}
                </Typography>
            </Box>
            <Paper elevation={3} sx={calendar_style.border}>
                <Stack sx={calendar_style.grid}>
                    <Stack direction="row" spacing={0} sx={calendar_style.grid}>
                        {_daysOfWeek.map((txt: string, inx: number) =>
                            <Box key = {inx} sx={calendar_style.gridItem}>
                                <Typography>{txt}</Typography>
                            </Box>
                        )}
                    </Stack>
                    {Array.from(Array(6)).map((_, _week: number) =>
                        <Stack direction="row" spacing={0} sx={calendar_style.grid}>
                            {Array.from(Array(7)).map((_, _day: number) =>
                                <Box key = {_day} sx={calendar_style.gridItem}>
                                    {_renderDay(_week, _day)}
                                </Box>
                            )}
                        </Stack>
                    )}
                </Stack>
            </Paper>
        </Stack>
    );
}

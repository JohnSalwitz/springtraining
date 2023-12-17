import GameDay from "./GameDay";
import {UNIT_TEST_SCHEDULE1} from "./test_data/UnitTestData";

describe('game day module', () => {

    it('converts a date', () => {
        const date = new Date("2024-02-22T13:10"+ "Z");
        expect(date.toDateString()).toBe("Thu Feb 22 2024")

        const d1 = new Date('March 5, 2024 13:00:00');
        const d2 = new Date("2024-03-05T13:10"+ "Z");
        expect(d1.toDateString()).toEqual(d2.toDateString())
        "2024-03-05T13:10"
    });

    it('gets the cumulative score for day', () => {
        let gameDay = new GameDay( UNIT_TEST_SCHEDULE1,  new Date('March 5, 2024 13:00:00'))
        expect(gameDay.score).toBe(18);
    });

    it('lists the game for the day', () => {
        let gameDay = new GameDay( UNIT_TEST_SCHEDULE1,  new Date('March 5, 2024 13:00:00'))
        expect(gameDay.toString()).toBe("");
    });
});
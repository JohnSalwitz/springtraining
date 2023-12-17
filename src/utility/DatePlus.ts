export class DatePlus extends Date {

    dayOfYear() : number {
        return this.getMonth() * 31 + this.getDate();
    }

    addDays(days: number): DatePlus {
        return new DatePlus(this.getTime() + days * 24 * 60 * 60 * 1000);
    }
}
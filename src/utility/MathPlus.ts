

export function Math_range(value: number, min: number, max: number) : number {
    return Math.max(Math.min(value,  max), min);
}
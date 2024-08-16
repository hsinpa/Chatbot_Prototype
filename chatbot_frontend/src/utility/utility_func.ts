export function Lerp( v0 : number,  v1 : number,  t : number) {
    return (1 - t) * v0 + t * v1;
}

export function GetImagePromise(imagePath : string) {
    return new Promise<HTMLImageElement>( resolve => {
        const im = new Image();
        im.crossOrigin = "anonymous";
        im.src = imagePath;
        im.onload = () => resolve(Object.assign(im));

        return im;
    });
}

export function GetRandomRange(min:number, max:number) {
    return Math.random() * (max - min) + min;
}

export function DoDelayAction(time : number) : Promise<void> {
    return new Promise(function (resolve, reject) {
        let flag = false;
        (
            function waitForFoo(){
                if (flag) return resolve();

                flag = true;
                setTimeout(waitForFoo, time);
        })();
    });
}

export function Clamp(value : number, min : number, max : number) {
    return Math.min(Math.max(value, min), max);
};

export function FormatString(string: string, params: any[]) {
return string.replace(/{(\d+)}/g, (match, index) => {
    return typeof params[index] !== 'undefined' ? params[index] : match;
});
}
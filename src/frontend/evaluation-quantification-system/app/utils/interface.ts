export interface User {
    admin   : boolean,
    student : boolean,
    username: string,
    userId  : string,
    isLogin : boolean,
    phone   : string,

}

export const defaultUser = {
    admin   : false,
    student : false,
    username: "",
    userId  : "",
    isLogin : false,
    phone   : "",
}
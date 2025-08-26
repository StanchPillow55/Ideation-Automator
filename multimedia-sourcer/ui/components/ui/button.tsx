import * as React from "react"; export function Button(p:React.ButtonHTMLAttributes<HTMLButtonElement>){const{className="",...r}=p;return <button className={`btn ${className}`} {...r}/>;}

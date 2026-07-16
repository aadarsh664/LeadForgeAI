import React from "react";
export function H1({ children, className = "" }: React.HTMLAttributes<HTMLHeadingElement>) { return <h1 className={`ds-typography-h1 ${className}`}>{children}</h1>; }
export function H2({ children, className = "" }: React.HTMLAttributes<HTMLHeadingElement>) { return <h2 className={`ds-typography-h2 ${className}`}>{children}</h2>; }
export function H3({ children, className = "" }: React.HTMLAttributes<HTMLHeadingElement>) { return <h3 className={`ds-typography-h3 ${className}`}>{children}</h3>; }
export function Text({ children, className = "" }: React.HTMLAttributes<HTMLParagraphElement>) { return <p className={`ds-typography-body ${className}`}>{children}</p>; }
export function Label({ children, className = "" }: React.HTMLAttributes<HTMLLabelElement>) { return <label className={`ds-typography-label ${className}`}>{children}</label>; }

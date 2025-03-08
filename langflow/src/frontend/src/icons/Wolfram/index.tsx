import React, { forwardRef } from "react";
import SvgWolfram from "./Wolfram";

export const WolframIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <SvgWolfram ref={ref} {...props} />;
});

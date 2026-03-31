import React from "react";

type GlassCardProps = {
  children: React.ReactNode;
  className?: string;
  as?: keyof JSX.IntrinsicElements;
};

function cn(...classes: Array<string | undefined>) {
  return classes.filter(Boolean).join(" ");
}

export default function GlassCard({
  children,
  className,
  as = "div",
}: GlassCardProps) {
  const Component = as as React.ElementType;

  return (
    <Component
      className={cn(
        "rounded-xl border border-white/10 bg-white/5 backdrop-blur-[12px]",
        className,
      )}
    >
      {children}
    </Component>
  );
}

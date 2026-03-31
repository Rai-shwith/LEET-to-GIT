import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
}

export function Button({
  variant = "primary",
  className = "",
  children,
  ...props
}: ButtonProps) {
  // Pill-shaped, modern base styles with flexbox for icon alignment and smooth active scaling
  const base =
    "inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full font-semibold transition-all duration-300 ease-out active:scale-[0.98]";

  // High-contrast, modern variants inspired by the reference design
  const variants = {
    // Primary: Vibrant gradient from Indigo to Cyan with a subtle glow
    primary:
      "bg-gradient-to-r from-[#4F46E5] to-[#06B6D4] text-white shadow-[0_4px_20px_rgba(6,182,212,0.3)] hover:shadow-[0_4px_25px_rgba(6,182,212,0.5)] hover:opacity-90",
    // Secondary: Dark, translucent with a subtle border (like "View Architecture" button)
    secondary:
      "bg-[#131326]/50 border border-[#2D2D5E] text-white hover:bg-[#2D2D5E]/50 backdrop-blur-md",
    // Danger: Red gradient for destructive actions
    danger:
      "bg-gradient-to-r from-[#EF4444] to-[#DC2626] text-white shadow-[0_4px_20px_rgba(239,68,68,0.3)] hover:shadow-[0_4px_25px_rgba(239,68,68,0.5)] hover:opacity-90",
  };

  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}

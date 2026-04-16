import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Tailwind-aware className merger. Used by every Shadcn-style primitive.
 * Shadcn convention: `cn()` combines conditional clsx inputs with
 * tailwind-merge's last-one-wins resolution across conflicting utilities.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

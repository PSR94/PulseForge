import { PulseShell } from "@/components/PulseShell";
import "../pulseforge-extra.css";

export default function WorkspaceLayout({children}:{children:React.ReactNode}) {
  return <PulseShell>{children}</PulseShell>;
}

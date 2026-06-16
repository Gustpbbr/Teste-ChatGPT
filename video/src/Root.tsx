import { Composition } from "remotion";
import { GusEncarnado } from "./GusEncarnado";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="GusEncarnado"
      component={GusEncarnado}
      durationInFrames={810}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};

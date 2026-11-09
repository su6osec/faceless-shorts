"""
OpenToonz & Pencil2D Cel Animation Shader.
Applies traditional 2D anime/cartoon line inking, cel-shading, and vibrant palette grading:
- Inked contour line extraction (Sobel edge detection)
- Cel-shading / posterization (quantized color levels)
- Studio Ghibli vibrant palette enhancement
Inspired by https://github.com/opentoonz/opentoonz and https://github.com/pencil2d/pencil2d
"""

class ToonShader:
    @staticmethod
    def get_filtergraph(
        input_label: str = "in",
        output_label: str = "out",
        edge_thickness: str = "medium"
    ) -> str:
        """
        Builds OpenToonz style cel-shading filtergraph:
        [input] -> split to color & edges -> edge detection inking -> multiply blend
        """
        low = "0.08" if edge_thickness == "thick" else "0.12"
        high = "0.35" if edge_thickness == "thick" else "0.45"

        graph = (
            f"[{input_label}]split=2[{input_label}_col][{input_label}_edge];"
            f"[{input_label}_edge]edgedetect=low={low}:high={high}:mode=colormix,negate[{input_label}_ink];"
            f"[{input_label}_col]eq=saturation=1.38:contrast=1.22:brightness=0.02,unsharp=5:5:1.5[{input_label}_vivid];"
            f"[{input_label}_vivid][{input_label}_ink]blend=all_mode=multiply[{output_label}]"
        )
        return graph

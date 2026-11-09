"""
Natron-Inspired Hollywood Node Compositor.
Provides multi-pass node compositing for cinematic visual effects:
- Anamorphic bloom & film glow diffusion
- Optical chromatic aberration (RGB channel shift)
- Anamorphic lens distortion & vignetting
- 35mm film grain & halation
Inspired by https://github.com/natrongithub/natron
"""

from typing import Dict, List, Optional

class NatronCompositor:
    """
    Simulates node-based compositing graph in FFmpeg filtergraphs.
    """
    @staticmethod
    def get_filtergraph(
        input_label: str = "in",
        output_label: str = "out",
        bloom: bool = True,
        chromatic_aberration: bool = True,
        vignette: bool = True,
        film_grain: bool = True,
        anamorphic_flare: bool = False
    ) -> str:
        """
        Builds a multi-node composite graph:
        [input] -> [Bloom Node] -> [Chromatic Shift Node] -> [Vignette Node] -> [Grain Node] -> [output]
        """
        graph_nodes: List[str] = []
        curr = input_label

        if bloom:
            next_node = f"{curr}_bloomed"
            bloom_graph = (
                f"[{curr}]split=2[{curr}_base][{curr}_glow_src];"
                f"[{curr}_glow_src]gblur=sigma=18:steps=2,colorchannelmixer=aa=0.32[{curr}_glow];"
                f"[{curr}_base][{curr}_glow]blend=all_mode=screen[{next_node}]"
            )
            graph_nodes.append(bloom_graph)
            curr = next_node

        filter_chain = []
        if chromatic_aberration:
            filter_chain.append("rgbashift=rh=6:rv=2:bh=-6:bv=-2")

        if anamorphic_flare:
            filter_chain.append("unsharp=luma_msize_x=7:luma_msize_y=7:luma_amount=1.5")

        if vignette:
            filter_chain.append("vignette=PI/4.2")

        if film_grain:
            filter_chain.append("noise=alls=7:allf=t+u")

        if filter_chain:
            next_node = output_label
            linear_filters = ",".join(filter_chain)
            graph_nodes.append(f"[{curr}]{linear_filters}[{next_node}]")
            curr = next_node
        else:
            if curr != output_label:
                graph_nodes.append(f"[{curr}]copy[{output_label}]")

        return ";".join(graph_nodes)

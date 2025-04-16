from HeyGenClient import HeyGenClient
import os

client = HeyGenClient()

client.generate_and_download_video(
    input_text="Are your luxury goods really what you think? Chinese TikTokers are exposing a hidden truth behind brands like Gucci and Louis Vuitton. As the US-China tariff war escalates, these digital whistleblowers are revealing that many luxury handbags are predominantly made in China. A video by senbags2, with over 10 million views, shows a factory worker claiming they've been the OEM—original equipment manufacturer—for major luxury brands for over 30 years. They allege brands repackage Chinese-made bags, adding logos for huge profits. While luxury brands try to move production elsewhere, TikTokers say they fail due to high costs and lower quality. With Chinese manufacturing wages far below those in the US, these workers are using TikTok to highlight the inequality and demand recognition for their skills. This exposé follows legal scrutiny of brands like Dior and Louis Vuitton for exploitative labor practices in Chinese-run factories.",
    output_path="output.mp4"
)
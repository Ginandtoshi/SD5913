# SD5913 Assignment 2 (2025.09.28)- Green Growth

This project visualizes an estimated China's forestry plantation data with generative pixel art on a terrain. Trees are planted and grow over time based on yearly plantation numbers and growth data. The image is also sectioned roughtly into regions, like northern, southern parts of China, where different trees would grow.

## Demo Video 
https://youtu.be/HWaw-RbZ5IM

## Inspiration
- I have always been interested in greenary and pixel arts. One of my prior classmates made a little grassland pixel animation with mini animal jumping in between the grass, which left me a deep inpression. Remembering that work and with my prior experience, I decided to search something relating to agriculture or forestry. 

## Data source
- Searching the web, there is very little open acess to exact, accurate, and uniformed China's forestry data; they are either outdated, collected in different formats, or not accessible for the general public. As a result, I asked DeepSeek-V3.1-Terminus to give me a simplified and estimated data by feeding the following sources:
    1) China Forestry and Grassland Statistical Yearbook (2018~2025) (中国林业和草原统计年鉴) http://202.99.63.178/c/www/tjnj.jhtml
    2) "National Forest Land Area Statistics, 1949-2018" (1949-2018年全国林地面积统计) https://zhuanlan.zhihu.com/p/370211655

Meanwhile, I chose the types of trees based on the following data collected by Timber Trade Portal https://www.timbertradeportal.com/zh/china/28/country-context and asked DeepSeek-V3.1-Terminus to summarize them into the table below: 
### 🌳 Top 10 Most Important Tree Species in Chinese Forestry
| Rank | Tree Species | Scientific Name | Ecological Importance | Economic Value | Cultural Significance | Key Characteristics | Primary Regions |
|------|--------------|-----------------|----------------------|----------------|------------------------|---------------------|-----------------|
| 1 | **Oak (栎树)** | *Quercus spp.* | - Foundation species in deciduous forests<br>- Supports high biodiversity<br>- Soil improvement through leaf litter | - High-quality timber<br>- Tannin production<br>- Animal fodder (acorns) | - Symbol of strength and longevity<br>- Important in traditional crafts | - Deep root system<br>- Lobed leaves<br>- Acorn fruits | Nationwide, especially temperate zones |
| 2 | **Birch (桦树)** | *Betula spp.* | - Pioneer species in succession<br>- Soil stabilization<br>- Supports fungal networks | - Ornamental use<br>- Birch sap products<br>- Plywood production | - Symbol of new beginnings<br>- Traditional paper making | - White peeling bark<br>- Catkin flowers<br>- Triangular leaves | Northern and northeastern China |
| 3 | **Larch (落叶松)** | *Larix spp.* | - Cold tolerance enables high-altitude growth<br>- Soil conservation in mountains<br>- Winter habitat | - Durable construction timber<br>- Resin production<br>- Railway sleepers | - Symbol of resilience in harsh conditions | - Deciduous conifer<br>- Needles in clusters<br>- Cones with thin scales | Northern China, high elevations |
| 4 | **Masson Pine (马尾松)** | *Pinus massoniana* | - Major component of southern forests<br>- Erosion control on slopes<br>- Wildlife habitat | - Rosin and turpentine production<br>- Pulp for paper<br>- Construction material | - Important in local economies of southern China | - Long needles (2 per bundle)<br>- Reddish bark<br>- Oval cones | Southern and eastern China |
| 5 | **Yunnan Pine (云南松)** | *Pinus yunnanensis* | - Adapted to plateau conditions<br>- Watershed protection<br>- Prevents soil erosion | - Local timber source<br>- Resin production<br>- Fuelwood | - Key species for ethnic minority regions | - Long, flexible needles (3 per bundle)<br>- Thick bark<br>- Large cones | Yunnan-Guizhou Plateau |
| 6 | **Spruce (云杉)** | *Picea spp.* | - Cold climate specialist<br>- Carbon sequestration<br>- Alpine ecosystem foundation | - High-quality resonance wood<br>- Christmas trees<br>- Musical instruments | - Symbol of northern wilderness | - Sharp, square needles<br>- Pendulous cones<br>- Pyramid shape | Northeastern and western mountains |
| 7 | **Fir (冷杉)** | *Abies spp.* | - Old-growth forest component<br>- Moisture regulation<br>- Subalpine zone stability | - Specialty wood products<br>- Paper manufacturing<br>- Essential oils | - Associated with sacred mountains | - Flat, soft needles<br>- Upright cones<br>- Smooth bark | Mountainous regions nationwide |
| 8 | **Cypress (柏树)** | *Cupressus spp.* | - Drought resistance<br>- Windbreak capabilities<br>- Long-term soil conservation | - Fragrant, durable wood<br>- Landscaping<br>- Traditional architecture | - Symbol of longevity<br>- Temple plantings | - Scale-like leaves<br>- Conical shape<br>- Small, woody cones | Widely planted, various habitats |
| 9 | **China Fir (杉木)** | *Cunninghamia lanceolata* | - Fast-growing for quick canopy closure<br>- Improves degraded lands<br>- Moderate water consumption | - Major timber species<br>- Fast rotation cycles<br>- Construction and furniture | - Traditional "feng shui" tree<br>- Village plantings | - Soft, fragrant wood<br>- Spiral leaf arrangement<br>- Peeling bark | Southern China, traditional plantations |
| 10 | **Alpine Pine (高山松)** | *Pinus densata* | - High-altitude specialist (>3000m)<br>- Timberline formation<br>- Soil stabilization in extreme conditions | - Limited but valuable timber<br>- Ecological restoration<br>- Climate change monitoring | - Symbol of high mountain ecosystems | - Short, stiff needles<br>- Dense growth form<br>- Small cones | Tibetan Plateau, high mountains |

Among these, I chose **Oak, Birch, Yunnan Pine, and China Fir** as my main assets for their distinct individual appearances and cultural representation.

## Resources Used
- VScode & Copilot - coding
- pixellab.ai - image assets creation https://www.pixellab.ai/
- procreate - image assets drawing
- pixabay - sound effect https://pixabay.com/sound-effects/search/game%20click/

## Project Structure
- `assets/` — For pixel art tree images，terrain backgrounds, and interactive sound effect.
- `forest_area.csv/` — For forestry data files (csv)
- `main.py` — Python code for data ingestion, visualization, and art generation
- `.github/copilot-instructions.md` — Workspace instructions for Copilot
- `README.md` — Project overview and usage instructions

## Dependencies
- `matplotlib` — For visualization
- `numpy` — For data manipulation
- `Pillow` — For image creation and editing
- `pygame`- For interaction




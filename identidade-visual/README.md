# Identidade visual: Engenharia Animada

Mesmo estilo e paleta do piloto EP01: low-poly, cores chapadas, sombra suave e fonte Montserrat Black.

| Arquivo | Uso |
|---|---|
| `perfil_800x800.png` | Foto de perfil. É o mascote **Eng. Carlin** com o nome escrito numa faixa branca em volta do capacete, curvada acompanhando a cúpula, sobre fundo azul com raios e anel amarelo. O nome a usar fica em `HELMET_NAME`, no `cena_identidade.py`. |
| `banner_2560x1440.png` | Capa do canal. Título, faixa de slogan, mascote e caldeira ficam dentro da área segura central (1546x423). Guindaste, viga caixão e contêineres ficam de fora e só aparecem no desktop ou na TV. |
| `previas/perfil_em_circulo.jpg` | O perfil recortado em círculo, em 800, 176, 88 e 48 px. |
| `previas/banner_guia_area_segura.jpg` | Banner com as marcações da área segura e da faixa do desktop. |
| `previas/banner_celular_1546x423.jpg`, `previas/banner_desktop_2560x423.jpg` | Como o banner aparece no celular e no desktop. |

## Paleta
Céu `#e6f4fb`→`#6fbde8` · chão `#e7d6ae` · azuis `#2f6fa3` / `#58a6d6` · laranja `#f29e4c` / colete `#ff7a1f` · amarelo guindaste `#f5c242` · capacete `#ffd23f` · contorno `#161616`.

## Como gerar de novo
```bash
identidade-visual/scripts/gerar.sh
```
- `scripts/cena_identidade.py` monta as cenas 3D no Blender 3.6 (EEVEE). Reaproveita o mascote e os materiais de `piloto-ep01/scripts/lowpoly_lib.py`.
- `scripts/compor.py` faz no Pillow o fundo do perfil, o título com contorno, a faixa de slogan e as prévias.
- `assets/Montserrat-Black.ttf` é uma instância estática (peso 900) da Montserrat variável, gerada com `fonttools varLib.instancer --remove-overlaps`. A versão variável deixa o "A" sem o vão no texto 3D do Blender. Licença: SIL Open Font License.

#!/usr/bin/env python
# coding=utf-8
import inkex
import math
import sys
from lxml import etree

class RegularPolygonGenerator(inkex.EffectExtension):
    count=0;
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--fractal_deep",    type=int, default=5, help="Fractal deep")
        pars.add_argument("--triangle_size",   type=float, default=100.0, help="Triangle size")
        pars.add_argument("--color_in_string", type=str, default="#000000", help="Color ex: black or #000000")




    def integer_to_rgba(self, color_value):
        # Se a cor for uma string no formato hexadecimal, converta para inteiro
        if isinstance(color_value, str):
            color_value = int(color_value.lstrip('#'))
        
        # Extrair componentes RGBA (assumindo que o valor é no formato 0xAARRGGBB)
        red = (color_value >> 24) & 0xFF   # Extrair alfa (primeiros 8 bits)
        green = (color_value >> 16) & 0xFF      # Extrair vermelho (seguintes 8 bits)
        blue = (color_value >> 8) & 0xFF     # Extrair verde (seguindo os 8 bits)
        alfa = color_value & 0xFF            # Extrair azul (últimos 8 bits)

        # Converter para o formato hexadecimal #RRGGBB (sem o componente alpha)
        hex_color = f"#{red:02X}{green:02X}{blue:02X}"
        
        
        return hex_color, f"{alfa/255.0}"

    def triangle_points(self,x,y,size):
        x3=x+size/2.0
        y3=y+size*math.pow(3,0.5)/2.0
        points = [f"{x},{y}", f"{x+size},{y}",f"{x3},{y3}"]
        return points

    def add_triangle(self,x,y,size,color):
        points=self.triangle_points(x,y,size);
        
        polygon = etree.Element(
            inkex.addNS("polygon", "svg"),
            {
                "points": " ".join(points),
                "style": "fill:"+color+";stroke:none"
            },
        )
        self.svg.get_current_layer().append(polygon)

    def draw_sierpinski(self,x, y, size, depth,color):
        if depth == 0:
            # Preenche o quadrado central
            self.add_triangle(x,y,size,color)
            
        else:
            # Divide em 9 partes e desenha os subquadrados
            new_size = size / 2.0

            self.draw_sierpinski(
                x, y,
                new_size,
                depth - 1,
                color
            )
            
            self.draw_sierpinski(
                x + size / 2.0, y,
                new_size,
                depth - 1,
                color
            )
            
            self.draw_sierpinski(
                x + size / 4.0, y + new_size*math.pow(3,0.5)/2,
                new_size,
                depth - 1,
                color
            )


    def effect(self):
        fractal_deep = self.options.fractal_deep
        triangle_size = self.options.triangle_size
        color_in_string = self.options.color_in_string;
        
        color_hex, opacity=self.integer_to_rgba(color_in_string);
        
        self.draw_sierpinski(0, 0, triangle_size, fractal_deep,color_hex)

if __name__ == "__main__":
    RegularPolygonGenerator().run()


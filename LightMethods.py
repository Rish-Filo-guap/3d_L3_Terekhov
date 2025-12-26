from dataclasses import dataclass
from typing import Tuple

import numpy as np


def lambert_lighting(normal, vectors, base_color=(1, 1, 1), light_intensity=1.0):

    light_dir=vectors['light']
    normal = np.array(normal, dtype=np.float32)
    light_dir = np.array(light_dir, dtype=np.float32)

    # нормализация векторов
    normal = normal / np.linalg.norm(normal)
    light_dir = light_dir / np.linalg.norm(light_dir)

    # расчет освещения
    cos_theta = np.dot(normal, light_dir)
    cos_theta = max(0, cos_theta)
    illumination = cos_theta * light_intensity

    # Применяем освещение к базовому цвету
    result_color = tuple(float(component * illumination) for component in base_color)
    return result_color





@dataclass
class Material:
    ambient: Tuple[float, float, float]  # фоновый цвет
    diffuse: Tuple[float, float, float]  # диффузный цвет
    specular: Tuple[float, float, float]  # зеркальный цвет
    shininess: float  # коэффициент блеска

@dataclass
class Light:
    direction: np.ndarray  # направление света
    color: Tuple[float, float, float]  # цвет света
    intensity: float = 1.0  # интенсивность света

def normalize_vector(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm



def phong_blinn_lighting(
        normal: Tuple[float, float, float],  # нормаль в точке
        vectors,# направление света
        ambient_intensity: float = 0.1  # интенсивность фонового освещения
) -> [float, float, float]:


    view_dir=vectors['camera']
    light_dir=vectors['light']

    material= Material(
        ambient=(0.0, 0.0, 0.0),      # слабый красный фон
        diffuse=(0.7, 0.7, 0.7),      # красный диффузный
        specular=(1.0, 1.0, 1.0),     # белый зеркальный
        shininess=32.0                # коэффициент блеска
    )

    light_intensity=0.8
    light_color=(1.0, 1.0, 1.0),  # белый свет

    N = normalize_vector(np.array(normal))  # нормаль
    V = normalize_vector(np.array(view_dir))  # направление взгляда
    L = normalize_vector(np.array(light_dir))  # направление К источнику света




    # (ambient)
    ambient = np.array(material.ambient) * ambient_intensity

    #  (diffuse)
    cos_theta = max(0.0, np.dot(N, L))
    diffuse = np.array(material.diffuse) * light_intensity * cos_theta * np.array(light_color)

    #  (specular)

    H = normalize_vector(L + V)  # полувектор
    cos_alpha = max(0.0, np.dot(N, H))

    specular = np.array(material.specular) * light_intensity * (cos_alpha ** material.shininess) * np.array(light_color)
    color = ambient + diffuse + specular

    return color[0].tolist()





def torrance_sparrow_illumination(

        normal,
        vectors,

        kd: np.ndarray = np.array([0.8, 0.8, 0.8]),  # Коэффициент диффузного отражения [r, g, b]
        ks: np.ndarray = np.array([1.0, 1.0, 1.0]),  # Коэффициент зеркального отражения [r, g, b]
        roughness: float = 0.1,  # Шероховатость поверхности (0-1, где 0 - идеально гладкая)
        F0: np.ndarray = np.array([0.04, 0.04, 0.04]),  # Коэффициент Френеля при нормальном падении
        light_intensity: np.ndarray = np.array([1.0, 1.0, 1.0])  # Интенсивность света [r, g, b]
) -> [float, float, float]:


    view_dir = vectors['camera']
    light_dir = vectors['light']

    # Нормализуем вектора
    normal = normal / np.linalg.norm(normal)
    light_dir = light_dir / np.linalg.norm(light_dir)
    view_dir = view_dir / np.linalg.norm(view_dir)

    # Вектор полунаправления (halfway vector)
    half_dir = light_dir + view_dir
    half_dir = half_dir / np.linalg.norm(half_dir)

    # Косинусы углов
    NdotL = max(0.0, np.dot(normal, light_dir))
    NdotV = max(0.0, np.dot(normal, view_dir))
    NdotH = max(0.0, np.dot(normal, half_dir))
    VdotH = max(0.0, np.dot(view_dir, half_dir))

    if NdotL <= 0.0 or NdotV <= 0.0:
        return [0.0, 0.0, 0.0]

    #  Диффузная компонента
    diffuse = kd * NdotL

    #  Геометрический фактор
    def G1(cos_theta, alpha):
        cos2 = cos_theta * cos_theta
        tan2 = (1 - cos2) / cos2 if cos2 > 0 else 0
        return 2.0 / (1 + np.sqrt(1 + alpha * alpha * tan2))

    alpha = roughness * roughness
    G = G1(NdotL, alpha) * G1(NdotV, alpha)

    def D_GGX(NdotH, alpha):
        if NdotH <= 0:
            return 0.0

        alpha2 = alpha * alpha
        NdotH2 = NdotH * NdotH
        denom = NdotH2 * (alpha2 - 1.0) + 1.0
        return alpha2 / (np.pi * denom * denom)

    D = D_GGX(NdotH, alpha)

    def fresnel_schlick(VdotH, F0):
        return F0 + (1.0 - F0) * ((1.0 - VdotH) ** 5)

    F = fresnel_schlick(VdotH, F0)

    # зеркальная компонента
    denominator = 4.0 * NdotV * NdotL + 1e-8
    specular = (D * F * G) / denominator

    color = light_intensity * (diffuse * (1.0 - F0) + ks * specular)


    color = np.clip(color, 0.0, 1.0)

    return color


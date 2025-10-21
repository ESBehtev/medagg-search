from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class DatasetCard:
    id: str
    title: str
    abstract: str
    modality: List[str]
    organs: List[str]
    diseases: List[str]
    tasks: List[str]
    population: List[str]
    size: int
    license: str
    year: int
    link: str

def synthetic_datasets() -> List[DatasetCard]:
    D = [
        DatasetCard(
            id="ds1",
            title="Lung CT for Pneumonia Classification",
            abstract="Multicenter chest CT dataset with confirmed pneumonia cases; includes non-contrast scans for adult patients.",
            modality=["CT"], organs=["lung","chest"], diseases=["pneumonia"],
            tasks=["classification"], population=["adult"], size=3500,
            license="CC-BY-NC", year=2023, link="https://example.org/ds1"
        ),
        DatasetCard(
            id="ds2",
            title="Brain MRI Tumor Segmentation (Glioma)",
            abstract="T1/T2/FLAIR MRI volumes for brain glioma with voxel-wise expert masks for segmentation tasks.",
            modality=["MRI"], organs=["brain"], diseases=["glioma","tumor"],
            tasks=["segmentation"], population=["adult"], size=1500,
            license="CC-BY", year=2022, link="https://example.org/ds2"
        ),
        DatasetCard(
            id="ds3",
            title="Diabetic Retinopathy Fundus Photos",
            abstract="Retinal fundus images for diabetic retinopathy grading with five-class labels; pediatric subset included.",
            modality=["Fundus"], organs=["retina","eye"], diseases=["diabetic retinopathy","diabetes"],
            tasks=["classification"], population=["adult","pediatric"], size=35000,
            license="CC-BY", year=2021, link="https://example.org/ds3"
        ),
        DatasetCard(
            id="ds4",
            title="Chest X-Ray COVID-19 Detection",
            abstract="CXR images from multiple hospitals with covid-19 positives and controls; de-identified and curated.",
            modality=["CXR"], organs=["chest","lung"], diseases=["covid-19","pneumonia"],
            tasks=["detection","classification"], population=["adult"], size=12000,
            license="CC-BY", year=2020, link="https://example.org/ds4"
        ),
        DatasetCard(
            id="ds5",
            title="Pathology Slides for Skin Melanoma",
            abstract="WSI dermatopathology slides with melanoma annotations for tile-based classification and detection.",
            modality=["Histopathology"], organs=["skin"], diseases=["melanoma","skin cancer"],
            tasks=["classification","detection"], population=["adult"], size=8000,
            license="CC-BY", year=2024, link="https://example.org/ds5"
        ),
        DatasetCard(
            id="ds6",
            title="ECG Arrhythmia Dataset",
            abstract="12-lead ECG recordings with arrhythmia labels; includes adolescent subjects.",
            modality=["ECG"], organs=["heart"], diseases=["arrhythmia"],
            tasks=["classification"], population=["adult","pediatric"], size=100000,
            license="PhysioNet-Restricted", year=2019, link="https://example.org/ds6"
        ),
        DatasetCard(
            id="ds7",
            title="Abdominal CT Liver Lesion Segmentation",
            abstract="Contrast and non-contrast abdominal CT volumes with lesion masks for liver tumor segmentation.",
            modality=["CT"], organs=["liver","abdomen"], diseases=["liver lesion","tumor"],
            tasks=["segmentation"], population=["adult"], size=2100,
            license="CC-BY-NC", year=2024, link="https://example.org/ds7"
        ),
        DatasetCard(
            id="ds8",
            title="EEG Seizure Detection Corpus",
            abstract="Scalp EEG recordings with seizure onset annotations; pediatric focus.",
            modality=["EEG"], organs=["brain"], diseases=["epilepsy","seizure"],
            tasks=["detection"], population=["pediatric"], size=7500,
            license="Open", year=2018, link="https://example.org/ds8"
        ),
        DatasetCard(
            id="ds9",
            title="Ultrasound Fetal Biometry",
            abstract="Obstetric ultrasound (US) images with measurements for gestational age estimation.",
            modality=["US"], organs=["fetus"], diseases=["pregnancy"],
            tasks=["regression"], population=["pediatric","neonatal"], size=6400,
            license="CC-BY", year=2022, link="https://example.org/ds9"
        ),
        DatasetCard(
            id="ds10",
            title="Retina OCT Fluid Segmentation",
            abstract="Optical coherence tomography (OCT) B-scans with expert fluid masks for segmentation tasks.",
            modality=["OCT"], organs=["retina","eye"], diseases=["amd","diabetic macular edema"],
            tasks=["segmentation"], population=["adult"], size=5200,
            license="CC-BY", year=2023, link="https://example.org/ds10"
        ),
        DatasetCard(
            id="ds11",
            title="Chest CT Lung Cancer Screening",
            abstract="Low-dose CT scans for lung cancer screening in smokers; multi-center longitudinal cohort.",
            modality=["CT"], organs=["lung","chest"], diseases=["lung cancer"],
            tasks=["classification","detection"], population=["adult"], size=25000,
            license="DUA", year=2024, link="https://example.org/ds11"
        ),
        DatasetCard(
            id="ds12",
            title="Clinical Notes De-identification",
            abstract="English ICU clinical notes with PHI entities annotated for NER de-identification.",
            modality=["Text"], organs=[], diseases=[], tasks=["ner","de-identification"],
            population=["adult"], size=200000, license="DUA", year=2017, link="https://example.org/ds12"
        ),
    ]
    return D

def to_public_dict(card: DatasetCard) -> Dict[str, Any]:
    return asdict(card)
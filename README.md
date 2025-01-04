## Repo Structure

```
.
├── copysyn_hifiganv1
├── copysyn_hifiganv1_norm_trim
├── gt_22.05k
├── gt_24k
├── gt_48k
├── gt_trans
├── README.md
├── scripts
├── xtts_22.05k
├── xtts_22.05k_norm_trim
└── xtts_24k
```

All processing scripts are under ```scripts```.

### Subjective Evaluation

System A (i.e. copy-synthesis) is obtained by:
1) downsampling: use ```scripts/02_downsample_gt.sh``` to convert ```gt_48k``` into ```gt_22.05k```
2) copy-synthesis: use ```scripts/11_copysynthesis.sh``` to convert ```gt_22.05k``` into ```copysyn_hifiganv1``` (note that the [HiFiGAN repo](https://github.com/jik876/hifi-gan) and the [released pretrained model](https://drive.google.com/drive/folders/1vJlfkwR7Uyheq2U5HrPnfTm-tzwuNuey?usp=drive_link) is required)
3) normalisation and add/clip silence at beginning/end: use ```scripts/12_norm_trim_copysyn.sh``` to convert ```copysyn_hifiganv1``` into ```copysyn_hifiganv1_norm_trim``` (NOTE THAT THERE ARE ISSUES - normalisation make background noise and breathy voices more apparaent and trimming cannot be done well using naive dB threshold)

System B (i.e. xtts2) is obtained by:
1) inference: use ```scripts/21_inference_xtts2.sh``` to convert ```gt_48k``` into ```xtts_24k``` (note that the [coqui-TTS repo](https://github.com/coqui-ai/TTS) and the [released model](https://huggingface.co/coqui/XTTS-v2) is required)
2) downsampling: use ```scripts/22_downsample_xtts2.sh``` to convert ```xtts_24k``` into ```xtts_22.05k```
3) normalisation and add/clip silence at beginning/end: use ```scripts/23_norm_trim_xtts2.sh``` to convert ```xtts_22.05k``` into ```xtts_22.05k_norm_trim``` (this is okay)

### Objective Evaluation

For objective evaluation, I recommend sticking to the same audios for subjective evaluation, i.e. ```copysyn_hifiganv1``` and ```xtts_22.05k_norm_trim```. I am not sure how certain acoustic features will be changed due to normalisation etc - so it would be worth checking.

I will add more accents/processed data as the experiments develop. I recommend starting with a few speakers (check if Edinburgh speaker A is closer to Edinburgh speaker B than Dublin speaker C in terms of metric xxx, yyy, ...)/

## Data Composition

1. This repo currently contains the ground truth / copy-synthesis / xtts2 generation of the rainbow passage of the following speakers in the VCTK corpus.

| ID | AGE | GENDER | ACCENTS | REGION | COMMENTS |
| -- | --- | ------ | ------- | ------ | -------- |
| p252 | 22 | M | Scottish | Edinburgh ||
| p262 | 23 | F | Scottish | Edinburgh ||
| p272 | 23 | M | Scottish | Edinburgh ||
| p281 | 29 | M | Scottish | Edinburgh ||
| p285 | 21 | M | Scottish | Edinburgh ||
| p245 | 25 | M | Irish | Dublin ||
| p288 | 22 | F | Irish | Dublin ||
| p295 | 23 | F | Irish | Dublin ||
| p340 | 18 | F | Irish | Dublin ||
| p225 | 23 | F | English | Southern England ||
| p228 | 22 | F | English | Southern England ||
| p229 | 23 | F | English | Southern England ||
| p231 | 23 | F | English | Southern England ||
| p232 | 23 | M | English | Southern England ||


## Data Issues

1. Some of the speech-text pairs in the VCTK corpus is missing. Out of the Edinburgh and Dublin accents, these files are missing.

- p272/p272_001_mic1.flac
- p281/p281_001_mic1.flac
- p295/p295_001_mic1.flac
- p295/p295_023_mic1.flac
- p295/p295_024_mic1.flac
- p340/p340_023_mic1.flac
- p225/p225_015_mic1.flac
- p228/p228_017_mic1.flac
- p231/p231_022_mic1.flac

2. Some recordings of the rainbow passage (the 001 to 024 utterances of each speaker) are uttered slightly differently as below.

| transcript file | transcription of this file | transcription of other files |
| - | - | - |
| gt_trans/Dublin/p295/p295_016.txt | The Norsemen considered the rainbow as a bridge over which the gods passed from *the* earth to their home in the sky. | The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.
| gt_trans/Dublin/p340/p340_006.txt | When the sunlight strikes *the* raindrops in the air, they act as a prism and form a rainbow. | When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow.
| gt_trans/Dublin/p340/p340_017.txt | Others have tried to explain *this* phenomenon physically. | Others have tried to explain the phenomenon physically. |
| gt_trans/Dublin/p245/p245_016.txt | *(The)* Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky. | The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.
| gt_trans/Edinburgh/p252/p252_021.txt | The difference in the rainbow depends considerably upon the size of the drops, and the width of the colored *bands* increases as the size of the drops increases. | The difference in the rainbow depends considerably upon the size of the drops, and the width of the colored band increases as the size of the drops increases.
| gt_trans/Edinburgh/p252/p252_022.txt | The actual primary rainbow observed is said to be the effect of super-*position* of a number of bows. | The actual primary rainbow observed is said to be the effect of super-imposition of a number of bows.
| gt_trans/SouthernEngland/p231/p231_016.txt | The Norsemen considered the rainbow as a bridge over which the gods passed from *the* earth to their home in the sky. | The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.

*italic* words are the parts misread during recording. *(xxx)* denotes the missing part during recording.



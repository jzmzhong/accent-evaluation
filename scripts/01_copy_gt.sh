# flacs
SRC_DIR="/work/tc062/tc062/jzmzhong/data/vctk_v0.92/wav48_silence_trimmed"
TAR_DIR="../gt_48k/Edinburgh"
for SPK in p252 p272 p281 p285 p262
do
    mkdir -p $TAR_DIR/$SPK
    for n in $(seq -f "%03g" 1 24)
    do
        cp $SRC_DIR/$SPK/${SPK}_${n}_mic1.flac $TAR_DIR/$SPK
    done
done
TAR_DIR="../gt_48k/Dublin"
for SPK in p288 p295 p340 p245
do
    mkdir -p $TAR_DIR/$SPK
    for n in $(seq -f "%03g" 1 24)
    do
        cp $SRC_DIR/$SPK/${SPK}_${n}_mic1.flac $TAR_DIR/$SPK
    done
done

# transcripts
SRC_DIR="/work/tc062/tc062/jzmzhong/data/vctk_v0.92/txt"
TAR_DIR="../gt_trans/Edinburgh"
for SPK in p252 p272 p281 p285 p262
do
    mkdir -p $TAR_DIR/$SPK
    for n in $(seq -f "%03g" 1 24)
    do
        cp $SRC_DIR/$SPK/${SPK}_${n}.txt $TAR_DIR/$SPK
    done
done
TAR_DIR="../gt_trans/Dublin"
for SPK in p288 p295 p340 p245
do
    mkdir -p $TAR_DIR/$SPK
    for n in $(seq -f "%03g" 1 24)
    do
        cp $SRC_DIR/$SPK/${SPK}_${n}.txt $TAR_DIR/$SPK
    done
done

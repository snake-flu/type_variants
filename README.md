# type_variants

A python script to type predefined variants in a fasta-format alignment of SARS-CoV-2 sequences, which **must be aligned to Wuhan-Hu-1**. See the [Genbank entry](https://www.ncbi.nlm.nih.gov/nuccore/MN908947.3) and the file `MN908947.fa` in this repository.

Pull requests welcome!

## Usage


The variants to type must be defined by the user in a config file (see the example `config.csv` in this repository).

This file has one line per variant of interest, and each line must be in one of the following three formats:

```
snp:T6954C
del:11288:9
aa:orf1ab:T1001I
```

Any `snp` lines should consist of a `:`-separated string whose first part is "snp" and whose second part describes the reference allele, the 1-based position of the site, and the alternative allele. 

Any `del` lines should consist of a `:`-separated string whose first part is "del", and whose second part is the 1-based first position of the deletion, and whose third part is the length of the deletion.

Any `aa` lines should consist of a `:`-separated string whose first part is "aa", and whose second part is the name of the coding sequence to query, and whose third part describes the reference amino acid, the 1-based number of the codon relative to the coding sequence it is in, and the alternative amino acid. 

For `snp` and `aa` lines, if the reference allele does not match the allele at the specified coordinates in the reference fasta file, the program will write an error to stderr and exit.

#### To run the program:

```
python3 type_variants.py --fasta-in query.fasta --variants-config config.csv --reference MN908947.fa --variants-out out.csv
```

Which will produce the file `out.csv`:

```
❯ head out.csv
query,ref_count,alt_count,other_count,fraction_alt
seq1,0,9,0,1.0
seq2,0,7,2,0.7778
seq3,0,9,0,1.0
seq4,0,9,0,1.0
seq5,0,9,0,1.0
seq6,0,9,0,1.0
seq7,0,9,0,1.0
seq8,0,9,0,1.0
seq9,0,9,0,1.0
...

```

`ref_count` is the total number of reference alleles in this query

`alt_count` is the total number of predefined alternative alleles in this query

`other_count` is the total number of alleles in this query that are neither `ref` nor `alt` - this includes other valid alleles as well as missing data.

`fraction_alt = alt_count / (ref_count + alt_count + other_count)`

#### Appending genotypes to the output

You can also append the genotype of each variant in the config file to the output with the `--append-genotypes` flag:

```
python3 type_variants.py --fasta-in query.fasta --variants-config config.csv --reference MN908947.fa --variants-out out.withgenotypes.csv --append-genotypes
```

```
❯ head out.withgenotypes.csv
query,ref_count,alt_count,other_count,fraction_alt,snp:C3267T,del:11288:9,aa:orf1ab:T1001I,del:21765:6,snp:G24914C,aa:S:N501Y,snp:A28111G,aa:Orf8:Q27*,aa:N:S235F
seq1,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
seq2,0,7,2,0.7778,T,X,I,X,C,Y,G,*,F
seq3,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
seq4,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
seq5,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
seq6,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
seq7,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
seq8,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
seq9,0,9,0,1.0,T,del,I,del,C,Y,G,*,F
...
```

Each genotype column contains the allele for that variant in each query sequence.

For amino acids, `X` denotes missing data/an untranslatable codon

For deletions, `X` denotes an allele that is neither the reference allele nor the deletion. Deletion variants are otherwise coded as `ref` (same nucleotide sequence as the reference) or `del`.

### Making an alignment in Wuhan-Hu-1 coordinates

If you have a consensus fasta file containing sequences that haven't been aligned to Wuhan-Hu-1, you can make an alignment to feed to this python script using [minimap2](https://github.com/lh3/minimap2), the latest version of [gofasta](https://github.com/cov-ert/gofasta) and the reference fasta file:

`minimap2 -a -x asm5 MN908947.fa unaligned.fasta | gofasta sam toMultiAlign > aligned.fasta`

Or potentially using [MAFFT](https://mafft.cbrc.jp/alignment/software/closelyrelatedviralgenomes.html) with the `--keeplength` option ("Keep alignment length" in the web app).

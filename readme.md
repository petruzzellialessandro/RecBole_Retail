# Retail RecBole

# Retail RecBole

## Preliminaries

Creare un env python nuovo e installare i requirements

## Struttura del progetto

Questo repository contiente l’implementazione di alcuni modelli presenti
nella libreria RecBole adattati ad un contesto Retail. Al progetto è
strutturato nel seguente modo:

- `raw_data`: In questa cartella ci sono i dati grezzi, non ancora
  processati per essere utilizzati dalla libreria. **Inserire in questa
  cartella i file `lines_hier.pkl` e `products.pkl`**
- `RECEIPT_LINES`: Cartella contente i dati che la libreria utilizza per
  addestrare e testare i modelli
- `model_type_1`: All’interno di questa cartella è presente il notebook
  per addestrare ed eseguire i modelli. Qui verranno create le cartelle
  per il salvataggio dei modelli e dei risultati sul test set.
- `model_type_2`: All’interno di questa cartella sono presenti due
  notebook notebook. Il primo è identico a quello presente nella
  cartella `model_type_1` (ed è giusto così, cambia il file di
  configurazione). Il secondo contiene le celle da eseguire per ottenere
  gli embedding a partire dalla gerarchia e salvare il file nel formato
  utilizzato dalla liberia. Il file sarà salvato nella cartella
  `RECEIPT_LINES` con estensione `.ent`.

# File importanti

- `dataset_creation.ipynb`: Questo file adatta il formato dei dati
  presenti nella cartella `raw_data` al formato preso in input dalla
  libreria.
- `config.yaml`: File di configurazione generale dei modelli. **Se non
  funziona qualcosa probabilmente il problema è qui.** Qui vanno
  specificati i path del dataset, gli iperparametri del modello, le
  metriche da calcolare, numero di epoche, etc. NB: modificare la voce
  `device` in `cpu` se non si possiede una GPU Nvidia su cui addestrare
  i modelli.

## Ordine di esecuzione

Dopo aver salvato nella cartella `raw_data` i file `lines_hier.pkl` e
`products.pkl`, eseguire tutte le celle del notebook
`dataset_creation.ipynb`. Al termine all’iterno della cartella
`RECEIPT_LINES` dovrebbero esser stati generati due file:

- `RECEIPT_LINES.inter`: file che modella i singoli acquisti con tutte
  le proprietà dello scontrino
- `RECEIPT_LINES.item`: file che modella i singoli prodotti con le loro
  proprietà (compresa la gerarchia)

## Modelli che non utilizzano la gerarchia

**NB**: Sebbene presenti nei file `RECEIPT_LINES.item` e
`RECEIPT_LINES.item`, i modelli ignorano i campi “attributi” sia degli
acquisti che dei prodotti.

Per eseguire i modelli che non utilizzano gli attributi eseguire le
celle presenti nel file `Models_Train_Test.ipynb` nella cartella
`model_type_1`, per ogni modello sono presenti due celle: la prima
addestra il modello, la seconda salva i risultati ottenuti sul test set
nella cartella `results` con il nome `{nome_modello}_test.json`.

## Modelli che utilizzano la gerarchia

Per eseguire i modelli che utilizzano la gerarchia si deve creare
prepare un file di embedding “pre-appresi”. Per farlo, eseguire tutte le
cella del notebook `prepare_embedding.ipynb`. Al termine nella cartella
`RECEIPT_LINES` sarò salvato il file `RECEIPT_LINES.ent` composto da due
colonne. Il codice identificato del file e l’embedding relativo. Per
addestrare i modelli che utilizzano questa informazione eseguire le
celle del file `Models_Train_Test.ipynb` nella cartella `model_type_2`.

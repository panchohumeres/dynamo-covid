0 21 * * * papermill /home/jovyan/work/ETL/covid-chile@min-ciencias.ipynb /home/jovyan/work/CRONTAB/logs/covid-chile@min-ciencias_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
40 21 * * * papermill /home/jovyan/work/ETL/chile-covid-derived@min-ciencias.ipynb /home/jovyan/work/CRONTAB/logs/covid-chile-derived@min-ciencias_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
40 21 * * * papermill /home/jovyan/work/ETL/chile-covid-derived@min-ciencias-50-53.ipynb /home/jovyan/work/CRONTAB/logs/covid-chile-derived@min-ciencias-50-53_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
#15 22 * * * papermill /home/jovyan/work/ETL/DEIS.ipynb /home/jovyan/work/CRONTAB/logs/DEIS_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
#45 22 * * * papermill /home/jovyan/work/ETL/Cuarentenas.ipynb /home/jovyan/work/CRONTAB/logs/Cuarentenas_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
#0 22 * * * papermill /home/jovyan/work/ETL/consolidado_nacional.ipynb /home/jovyan/work/CRONTAB/logs/consolidado_nacional_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
#10 0 * * *  papermill /home/jovyan/work/ETL/LOGLOG.ipynb /home/jovyan/work/CRONTAB/logs/LOGLOG_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
#0 0 * * SAT papermill /home/jovyan/work/ETL/movilidad.ipynb /home/jovyan/work/CRONTAB/logs/movilidad_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
26 */6 * * * papermill /home/jovyan/work/ETL/cleanETL.ipynb /home/jovyan/work/CRONTAB/logs/cleanETL_`date +\%Y\%m\%d\%H\%M\%S`.ipynb
0 */6 * * * papermill /home/jovyan/work/ETL/WORLD.ipynb /home/jovyan/work/CRONTAB/logs/WORLD_`date +\%Y\%m\%d\%H\%M\%S`.ipynb

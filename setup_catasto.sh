#scarico limiti catastali
wget https://194.105.54.191/IDT/vector/public/p_tn_f81f0f0d-5a6f-4e69-b951-3604cc4dbabe.zip -O limiti_comune_catastale.zip --no-check-certificate
unzip -o limiti_comune_catastale.zip
spatialite_tool -i -shp ammcat -d catasto.sqlite -t ammcat -c UTF-8 -s 25832
wget https://194.105.54.191/IDT/vector/public/p_tn_0dc5bc18-54de-4495-be3e-9e44f2135803.zip -O limiti_amministrativi.zip --no-check-certificate
unzip -o limiti_amministrativi.zip
spatialite_tool -i -shp ammcom -d catasto.sqlite -t ammcom -c UTF-8 -s 25832
wget https://194.105.54.191/IDT/vector/public/p_tn_1e93bc40-a91f-49ba-891d-de3a4627b86e.zip -O limiti_comprensoriale.zip --no-check-certificate
unzip -o limiti_comprensoriale.zip
spatialite_tool -i -shp ammcmp -d catasto.sqlite -t ammcmp -c UTF-8 -s 25832
wget https://194.105.54.191/IDT/vector/public/p_tn_58604ed2-ac1d-4f78-a00c-514fd3562c51.zip -O limiti_comunita_di_valle.zip --no-check-certificate
unzip -o limiti_comunita_di_valle.zip
spatialite_tool -i -shp p_tn_58604ed2-ac1d-4f78-a00c-514fd3562c51/ammcva -d catasto.sqlite -t ammcva -c UTF-8 -s 25832
python adapt_table.py catasto.sqlite amm
mkdir data
cd data
wget http://www.territorio.provincia.tn.it/geodati/catasto/2039_catasto_shp.zip -O catasto.zip
unzip -o catasto.zip
rm catasto.zip
for i in `ls *.zip`
do
name="`basename $i _shp.zip`_vl_parcel_poly"
unzip -o $i $name*
nname="`basename $i _shp.zip`"
spatialite_tool -i -shp $name -d ../catasto.sqlite -t $nname -c CP1252 -s 3044
python ../adapt_table.py ../catasto.sqlite $nname
done
cd ..
rm -fr data
rm -fr p_tn_58604ed2-ac1d-4f78-a00c-514fd3562c51
rm *.zip
rm amm*



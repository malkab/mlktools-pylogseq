- # Proceso de publicación
  - También presente en el **README.md**
      + [ ] publish new **libsunnsaasdef** if applicable;
      + [ ] initiate **tmuxinator profile sunnsaas-libsunnsaasbackend**;
      + [ ] full testing can be made on remote to save resources. If so, set a context and use **rsync.sh** / **ssh.sh** (see **Testing on Remote** below). All the following steps are performed the same in remote or locally;
      + [ ] Arrancar el persistence stack con **002**;
      + [ ] enter Docker **010-node_run**;
      + [ ] check outdated packages: **yarn outdated ; yarn upgrade**. If only testing a new version of the algorithm, decide if it's worth to upgrade, since a rebuild will be needed. Test the new algorithm just with current packages if there is no change to the code;
      + [ ] launch **yarn reset-tests ; yarn start and yarn start-new** for a full test run. Select tests to run by commenting on **main.test.ts**;
      + [ ] test **yarn build** if something changed in the code. If just testing a new version of the algorithm without changing anything, this is not needed;
      + [ ] run **yarn publish-dev**;
      + [ ] integrate new **libsunnsaasdef** and **libsunnsaasbackend** into **sunnsaas_v1**.

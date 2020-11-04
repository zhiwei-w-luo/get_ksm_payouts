# get_ksm_payouts

Clone https://github.com/paritytech/substrate-api-sidecar

cd substrate-api-sidecar

Create .env.kusama File with SAS_SUBSTRATE_WS_URL=wss://kusama-rpc.polkadot.io

yarn install

NODE_ENV=kusama yarn start

python3 get_ksm_payouts.py -a <address> -d <depth> -e <era>

### running-node:
![image](https://github.com/zhiwei-w-luo/get_ksm_payouts/blob/main/images/running-node.png)
### sidecar
![image](https://github.com/zhiwei-w-luo/get_ksm_payouts/blob/main/images/sidecar.png)
### result
![image](https://github.com/zhiwei-w-luo/get_ksm_payouts/blob/main/images/result.png)

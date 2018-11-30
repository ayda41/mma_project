{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Project():\n",
    "    def __init__(self, name, users):\n",
    "        self.project_name = name\n",
    "        self.project_users = users\n",
    "        hash_id = name\n",
    "        for i in users:\n",
    "            hash_id += i.name\n",
    "        self.id= hash(hash_id)\n",
    "        self.ledger = pd.DataFrame({\"project_id\": self.id, \n",
    "                                    \"transac_id\": [np.nan],\n",
    "                                    \"date\": [np.nan], \n",
    "                                    \"total_amount\": [np.nan],\n",
    "                                    \"people_name\": [np.nan], \n",
    "                                    \"payer_name\": [np.nan], \n",
    "                                    \"method\": [np.nan],\n",
    "                                    \"description\": [np.nan],\n",
    "                                    \"category\": [np.nan]},\n",
    "                                    dtype = 'object')\n",
    "        self.balance = {user.name: 0 for user in users}\n",
    "    \n",
    "        \n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

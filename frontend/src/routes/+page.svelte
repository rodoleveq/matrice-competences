<script>
	import { onMount } from 'svelte';
	import { getMatrixData, saveMatrixData } from '$lib/api.js';
    // Importez le nouveau composant
	import ProgressionCell from '$lib/components/ProgressionCell.svelte';

	let matrixData = { ranks: [], pillars: [] };
	let activeTab = 'restitution';
	let isLoading = true;
	let errorMessage = '';

	onMount(async () => {
		try {
			matrixData = await getMatrixData();
		} catch (error) {
			errorMessage = "Erreur de connexion avec le serveur backend. Vérifiez qu'il est bien lancé et qu'il n'y a pas d'erreur dans son terminal.";
			console.error(error);
		} finally {
			isLoading = false;
		}
	});

	async function handleSaveChanges() {
		try {
			await saveMatrixData(matrixData);
			alert('Changements sauvegardés avec succès !');
		} catch (error) {
			alert('Erreur lors de la sauvegarde des changements.');
			console.error(error);
		}
	}
    
	function addPillar() {
        const newValues = Array(matrixData.ranks.length).fill('');
		matrixData.pillars = [
			...matrixData.pillars,
			{
				name: 'Nouveau Pilier',
				colorClasses: { bg: 'bg-gray-50', text: 'text-gray-800', accent: 'bg-gray-200', icon: 'text-gray-600', border: 'border-gray-200' },
				items: [
					{ type: 'Progression (Eagle)', values: [...newValues] },
					{ type: 'Activités (Fiches)', values: [...newValues] }
				]
			}
		];
	}

	function removePillar(index) {
		if (confirm(`Supprimer le pilier "${matrixData.pillars[index].name}" ?`)) {
			matrixData.pillars.splice(index, 1);
			matrixData.pillars = matrixData.pillars;
		}
	}
</script>

<svelte:head>
	<title>Matrice de Compétences : Filière Delivery Manager</title>
</svelte:head>

<main class="p-4 md:p-8">
	<div class="max-w-full mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
        <header class="bg-gray-800 text-white p-6">
			<h1 class="text-2xl font-bold">Filière "Delivery Manager"</h1>
			<p class="text-gray-300 mt-1">Matrice de compétences interactive</p>
		</header>

		<div class="border-b border-gray-200">
			<nav class="flex -mb-px px-6">
				<button on:click={() => (activeTab = 'restitution')} class="py-4 px-1 border-b-2 text-sm font-medium" class:text-blue-600={activeTab === 'restitution'} class:border-blue-600={activeTab === 'restitution'} class:font-semibold={activeTab === 'restitution'} class:text-slate-600={activeTab !== 'restitution'} class:border-transparent={activeTab !== 'restitution'}>
					Restitution
				</button>
				<button on:click={() => (activeTab = 'gestion')} class="py-4 px-1 ml-8 border-b-2 text-sm font-medium" class:text-blue-600={activeTab === 'gestion'} class:border-blue-600={activeTab === 'gestion'} class:font-semibold={activeTab === 'gestion'} class:text-slate-600={activeTab !== 'gestion'} class:border-transparent={activeTab !== 'gestion'}>
					Gestion
				</button>
			</nav>
		</div>

		<div class="p-6">
			{#if isLoading}
				<p class="text-center text-gray-500">Chargement des données...</p>
			{:else if errorMessage}
				<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4" role="alert">
					<p class="font-bold">Erreur de connexion</p>
					<p>{errorMessage}</p>
				</div>
			{:else}
				<!-- Vue Restitution -->
				{#if activeTab === 'restitution'}
					<div class="overflow-x-auto">
						<table class="min-w-full border-collapse text-sm" style="border-spacing: 0 4px;">
							<thead class="bg-gray-100 sticky top-0 z-10">
								<tr>
									<th class="p-3 font-semibold text-left text-gray-700 w-1/12">Pilier</th>
									<th class="p-3 font-semibold text-left text-gray-700 w-1/12">Attendu</th>
									{#each matrixData.ranks as rank}
										<th class="p-3 font-semibold text-left text-gray-700 w-1/6">{rank}</th>
									{/each}
								</tr>
							</thead>
							<tbody>
								{#each matrixData.pillars as pillar}
									{#each pillar.items as item, itemIndex}
										<tr class="border-b-2 border-white {pillar.colorClasses.bg}">
											{#if itemIndex === 0}
												<td
													class="p-3 font-bold {pillar.colorClasses.text} align-top border-l-4 {pillar.colorClasses.border}"
													rowspan={pillar.items.length}>{pillar.name}</td>
											{/if}
											<td class="p-3 font-semibold text-gray-600 italic align-top">{item.type}</td>
											{#each item.values as value}
												{#if item.type.includes("Progression")}
                                                    <td class="p-3 text-gray-700 align-top">
                                                        <ProgressionCell text={value} colors={pillar.colorClasses} />
                                                    </td>
                                                {:else}
                                                    <td class="p-3 text-gray-700 align-top">{@html value.replace(/<br\/>/g, '<br/><br/>')}</td>
                                                {/if}
											{/each}
										</tr>
									{/each}
								{/each}
							</tbody>
						</table>
					</div>
				{/if}

				<!-- Vue Gestion -->
				{#if activeTab === 'gestion'}
                    <div class="bg-blue-50 border-l-4 border-blue-500 text-blue-700 p-4 rounded-md mb-6" role="alert">
                        <p class="font-bold">Mode Administration</p>
                        <p class="text-sm">Modifiez les textes, puis cliquez sur "Sauvegarder les changements".</p>
                    </div>
                    <div class="flex items-center space-x-4 mb-6">
                        <button on:click={handleSaveChanges} class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700">Sauvegarder</button>
                        <button on:click={addPillar} class="px-4 py-2 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-600">Ajouter un Pilier</button>
                    </div>
                    
                    <!-- Formulaires d'édition -->
                    {#each matrixData.pillars as pillar, pillarIndex}
                        <div class="mb-6 border rounded-lg shadow-sm bg-white">
                             <div class="p-4 bg-gray-50 rounded-t-lg flex justify-between items-center">
                                <input type="text" bind:value={pillar.name} class="text-xl font-bold text-gray-800 p-2 border rounded-md w-1/2"/>
                                <button 
                                    on:click={() => removePillar(pillarIndex)} 
                                    class="p-2 text-red-500 hover:bg-red-100 rounded-full"
                                    aria-label="Supprimer le pilier {pillar.name}"
                                >
                                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </div>
                            <div class="p-4 grid grid-cols-1 md:grid-cols-{matrixData.ranks.length} gap-4">
                                {#each pillar.items as item}
                                    {#each item.values as value, valueIndex}
                                        <div class="mt-2 flex flex-col">
                                            <label for="cell-{pillarIndex}-{item.type}-{valueIndex}" class="font-semibold text-gray-500 text-sm mb-1">{matrixData.ranks[valueIndex]} ({item.type})</label>
                                            <textarea 
                                                id="cell-{pillarIndex}-{item.type}-{valueIndex}"
                                                bind:value={item.values[valueIndex]} 
                                                class="w-full p-2 border rounded-md h-40 shadow-sm text-sm flex-grow"
                                            ></textarea>
                                        </div>
                                    {/each}
                                {/each}
                            </div>
                        </div>
                    {/each}
				{/if}
			{/if}
		</div>
	</div>
</main>


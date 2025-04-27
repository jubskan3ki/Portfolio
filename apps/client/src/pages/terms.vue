<template>
	<Section title="Mentions légales">
		<div class="legal-content">
			<h2>Informations légales</h2>
			<p>
				Conformément aux dispositions des articles 6-III et 19 de la Loi n° 2004-575 du 21 juin 2004 pour la
				Confiance dans l'économie numérique, dite L.C.E.N., nous portons à la connaissance des utilisateurs et
				visiteurs du site les informations suivantes :
			</p>

			<h3>1. Informations légales</h3>
			<div class="legal-info">
				<p><strong>Propriétaire du site :</strong> [Votre nom]</p>
				<p><strong>Adresse :</strong> [Votre adresse]</p>
				<p><strong>Email :</strong> [Votre email]</p>
				<p><strong>Statut :</strong> [Auto-entrepreneur / SARL / etc.]</p>
				<p><strong>Numéro SIRET :</strong> [Votre numéro SIRET]</p>
			</div>

			<h3>2. Hébergement</h3>
			<div class="legal-info">
				<p><strong>Hébergeur :</strong> [Nom de l'hébergeur]</p>
				<p><strong>Adresse :</strong> [Adresse de l'hébergeur]</p>
				<p><strong>Téléphone :</strong> [Téléphone de l'hébergeur]</p>
			</div>

			<h3>3. Conception et réalisation</h3>
			<p>Le site a été conçu et développé par [Votre nom / Votre entreprise].</p>

			<h3>4. Crédits</h3>
			<p>
				Les textes, images, logos et éléments graphiques sont la propriété de leurs auteurs respectifs.
				<br />
				Les photographies et illustrations utilisées sur ce site sont soit notre propriété, soit utilisées avec
				l'autorisation de leurs auteurs ou dans le cadre de licences spécifiques.
			</p>

			<h3>5. Cookies et données personnelles</h3>
			<p>
				Pour plus d'informations sur la manière dont nous utilisons les cookies et traitons vos données
				personnelles, veuillez consulter notre
				<NuxtLink to="/privacy">Politique de Confidentialité</NuxtLink>.
			</p>

			<h3>6. Propriété intellectuelle</h3>
			<p>
				L'ensemble du contenu de ce site, incluant sans limitation les textes, graphiques, logos, images, clips
				audio, est la propriété de [Votre nom / Votre entreprise] et est protégé par les lois françaises et
				internationales sur le droit d'auteur.
			</p>
			<p>
				Toute reproduction ou représentation totale ou partielle de ce site ou de son contenu par quelque
				procédé que ce soit, sans autorisation expresse, est interdite et constituerait une contrefaçon
				sanctionnée par les articles L.335-2 et suivants du Code de la propriété intellectuelle.
			</p>

			<h3>7. Loi applicable et juridiction</h3>
			<p>
				Le présent site est soumis à la loi française. En cas de litige, les tribunaux français seront seuls
				compétents.
			</p>
		</div>
	</Section>
</template>

<style lang="scss" scoped>
	.legal-content {
		max-width: 800px;
		margin: 0 auto;

		h2,
		h3 {
			margin-top: 2rem;
			margin-bottom: 1rem;
		}

		p {
			margin-bottom: 1rem;
			line-height: 1.6;
		}

		.legal-info {
			background-color: #f8f9fa;
			padding: 1.5rem;
			border-radius: 8px;
			margin-bottom: 1.5rem;

			p {
				margin-bottom: 0.5rem;

				&:last-child {
					margin-bottom: 0;
				}
			}
		}
	}
</style>

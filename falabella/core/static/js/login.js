document.addEventListener('DOMContentLoaded', function() {
    // Configuración del popover para el área de login
    const loginArea = document.getElementById('loginArea');
    const chevronIcon = document.getElementById('chevronIcon');
    
    if (loginArea && chevronIcon) {
        const popover = new bootstrap.Popover(chevronIcon, {
            trigger: 'manual',
            placement: 'bottom',
            html: true,
            content: `
                <div class="popover-body text-start">
                    <ul class="list-unstyled m-0">
                        <li class="mb-3">
                            <a href="#" class="semi-bold-on-hover no-underline" id="loginLink">
                                Inicia sesión
                            </a>
                        </li>
                        <li class="mb-3">
                            <a href="#" class="semi-bold-on-hover no-underline" id="registerLink">
                                Regístrate
                            </a>
                        </li>
                        <li class="mb-3">
                            <a href="#" class="semi-bold-on-hover no-underline" id="myAccountLink">
                                Mi cuenta
                            </a>
                        </li>
                        <hr class="my-3">
                        <li class="mb-3">
                            <a href="/" class="semi-bold-on-hover no-underline">CMR Puntos</a>
                        </li>
                    </ul>
                </div>
            `
        });

        // Mostrar/ocultar popover al hover
        loginArea.addEventListener('mouseenter', () => popover.show());
        loginArea.addEventListener('mouseleave', () => {
            setTimeout(() => {
                if (!loginArea.matches(':hover') && !document.querySelector('.popover:hover')) {
                    popover.hide();
                }
            }, 300);
        });

        // Mantener el popover visible mientras el mouse esté sobre él
        document.addEventListener('mouseover', (e) => {
            const popoverElement = document.querySelector('.popover');
            if (popoverElement && popoverElement.contains(e.target)) {
                popover.show();
            }
        });

        // Ocultar el popover cuando el mouse sale del área
        document.addEventListener('mouseleave', (e) => {
            const popoverElement = document.querySelector('.popover');
            if (popoverElement && !loginArea.contains(e.target) && !popoverElement.contains(e.target)) {
                popover.hide();
            }
        });
    }
});